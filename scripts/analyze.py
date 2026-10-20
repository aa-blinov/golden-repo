#!/usr/bin/env python3
"""analyze — read a repository and report what is actually in it.

    scripts/analyze.py <repository> [--owner aa-blinov] [--out facts.json]

The facts are the input to the documents. A README that says how to install
the software is written from the software's own metadata, not from a guess
about what a project like this would need.

The output is a JSON packet: the language and its runtime, the commands that
run and test the project, the direct dependencies, the shape of the source
tree, the entry points, the configuration the software reads, and what the
existing README already claims. The last one matters: the facts the owner has
already written are facts, and the documents keep them.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "out", "target", "vendor",
    ".venv", "venv", "__pycache__", ".next", ".nuxt", ".output", "coverage",
    "site-packages", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".gradle", ".idea", ".cache", "third_party", "third-party",
}

# The files that say what a project is made of.
MANIFESTS = [
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "Cargo.toml",
    "go.mod", "Makefile", "justfile", "requirements.txt", "requirements-dev.txt",
    "Gemfile", "composer.json", "pom.xml", "build.gradle", "build.gradle.kts",
    "CMakeLists.txt", "mix.exs", "pubspec.yaml", "deno.json", "bun.lockb",
]

# The files that say how to run it.
RUN_FILES = [
    "README.md", "AGENTS.md", "CLAUDE.md", "PRODUCT.md", "DESIGN.md",
    "CONTRIBUTING.md", "docs/README.md",
]


def run(args, cwd=None, check=False):
    result = subprocess.run(
        args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=check,
    )
    return result.stdout.decode("utf-8", "replace")


def read(path, limit=None):
    try:
        with open(path, "r", errors="replace") as handle:
            text = handle.read()
    except (IOError, OSError):
        return ""
    if limit and len(text) > limit:
        text = text[:limit]
    return text


def tree_of(root):
    """The source tree, at most three levels deep, directories included."""
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        dirnames[:] = sorted(
            d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
        )
        if depth >= 3:
            dirnames[:] = []
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            path = os.path.normpath(os.path.join(rel, name)) if rel != "." else name
            entries.append(path)
        if depth < 2:
            for name in dirnames:
                path = os.path.normpath(os.path.join(rel, name)) if rel != "." else name
                entries.append(path + "/")
    return sorted(set(entries))


def language_of(root, files):
    """The language, the runtime, and the package manager."""
    info = {"language": None, "runtime": None, "package_manager": None}

    if "package.json" in files:
        info["language"] = "JavaScript"
        info["runtime"] = "Node.js"
        info["package_manager"] = "npm"
        try:
            data = json.loads(read(os.path.join(root, "package.json")))
        except ValueError:
            data = {}
        if data.get("type") == "module" or any(
            p.endswith(".ts") for p in files
        ):
            info["language"] = "TypeScript"
        info["node_requirement"] = data.get("engines", {}).get("node")
        info["scripts"] = data.get("scripts", {})
        info["bin"] = data.get("bin")
        info["dependencies"] = sorted(
            k for k in data.get("dependencies", {}) if not k.startswith("@types/")
        )
        info["dev_dependencies"] = sorted(
            k for k in data.get("devDependencies", {}) if not k.startswith("@types/")
        )
        if "pnpm-lock.yaml" in files:
            info["package_manager"] = "pnpm"
        elif "yarn.lock" in files:
            info["package_manager"] = "yarn"

    if "pyproject.toml" in files:
        info["language"] = "Python"
        info["runtime"] = "Python"
        text = read(os.path.join(root, "pyproject.toml"))
        info["package_manager"] = "uv" if "uv.lock" in files else "pip"
        match = re.search(r'requires-python\s*=\s*"([^"]+)"', text)
        if match:
            info["python_requirement"] = match.group(1)
        match = re.search(r"\[project\.scripts\](.*?)(\n\[|\Z)", text, re.DOTALL)
        if match:
            info["scripts"] = dict(re.findall(r"^(\S+)\s*=\s*\"([^\"]*)\"", match.group(1), re.M))
        deps = re.search(r"dependencies\s*=\s*\[(.*?)\]", text, re.DOTALL)
        if deps:
            info["dependencies"] = re.findall(r'"([^"]+)"', deps.group(1))
        scripts = re.search(r"\[tool\.poetry\.scripts\](.*?)(\n\[|\Z)", text, re.DOTALL)
        if scripts:
            info["scripts"] = dict(
                re.findall(r"^(\S+)\s*=\s*\"([^\"]*)\"", scripts.group(1), re.M)
            )

    if "Cargo.toml" in files:
        info["language"] = "Rust"
        info["runtime"] = "Rust"
        info["package_manager"] = "cargo"
        text = read(os.path.join(root, "Cargo.toml"))
        deps = re.search(r"\[dependencies\](.*?)(\n\[|\Z)", text, re.DOTALL)
        if deps:
            info["dependencies"] = re.findall(r'^([a-zA-Z0-9_-]+)\s*=', deps.group(1), re.M)

    if "go.mod" in files:
        info["language"] = "Go"
        info["runtime"] = "Go"
        info["package_manager"] = "go"
        text = read(os.path.join(root, "go.mod"))
        match = re.search(r"^go\s+([\d.]+)", text, re.MULTILINE)
        if match:
            info["go_requirement"] = match.group(1)
        deps = re.search(r"require\s*\((.*?)\)", text, re.DOTALL)
        if deps:
            info["dependencies"] = re.findall(r"^\s*([a-z0-9./-]+)\s+v", deps.group(1), re.M)
        direct = re.search(r"require\s+([^\s(]+)\s+v", text)
        if direct:
            info.setdefault("dependencies", []).append(direct.group(1))

    if "requirements.txt" in files:
        info.setdefault("language", "Python")
        info.setdefault("package_manager", "pip")
        text = read(os.path.join(root, "requirements.txt"))
        info["dependencies"] = [
            line.split("==")[0].split(">=")[0].strip()
            for line in text.split("\n")
            if line.strip() and not line.startswith(("#", "-"))
        ]

    if info["language"] is None:
        counts = {}
        for path in files:
            ext = os.path.splitext(path)[1].lower()
            if ext in (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs",
                       ".rb", ".java", ".kt", ".swift", ".cs", ".php", ".ex",
                       ".exs", ".scala", ".dart", ".vue", ".svelte"):
                counts[ext] = counts.get(ext, 0) + 1
        if counts:
            ext = max(counts, key=counts.get)
            info["language"] = {
                ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
                ".jsx": "JavaScript", ".tsx": "TypeScript", ".go": "Go",
                ".rs": "Rust", ".rb": "Ruby", ".java": "Java", ".kt": "Kotlin",
                ".swift": "Swift", ".cs": "C#", ".php": "PHP", ".ex": "Elixir",
                ".exs": "Elixir", ".scala": "Scala", ".dart": "Dart",
                ".vue": "Vue", ".svelte": "Svelte",
            }.get(ext, ext)

    return info


def entry_points(root, files):
    """The files that start the software, and what they are."""
    points = []
    for path in files:
        base = os.path.basename(path)
        if base in ("main.py", "app.py", "__main__.py", "cli.py", "server.py",
                    "index.js", "index.ts", "main.go", "main.rs", "main.c"):
            points.append(path)
    for path in files:
        if re.search(r"(^|/)__main__\.py$", path):
            points.append(path)
    if "package.json" in files:
        try:
            data = json.loads(read(os.path.join(root, "package.json")))
            for name, path in (data.get("bin") or {}).items() if isinstance(
                data.get("bin"), dict
            ) else []:
                points.append(path)
        except ValueError:
            pass
    return sorted(set(points))[:20]


def configuration(root, files):
    """The files that hold configuration, and the environment variables the
    software reads."""
    config_files = []
    env_files = []
    env_vars = set()
    for path in files:
        base = os.path.basename(path)
        if base.startswith(".env"):
            env_files.append(path)
        if base in ("config.example.json", "config.example.yaml", "config.py",
                    "config.toml", "settings.py", "docker-compose.yml",
                    "compose.yml", "compose.yaml", "Dockerfile", "Caddyfile"):
            config_files.append(path)
        if base.endswith((".py", ".js", ".ts", ".go", ".rs")):
            text = read(os.path.join(root, path), 200000)
            for match in re.finditer(
                r"""(?:process\.env\.|os\.environ\[|os\.getenv\(|getenv\()\s*['"]([A-Z][A-Z0-9_]{3,})['"]""",
                text,
            ):
                env_vars.add(match.group(1))
            for match in re.finditer(r"^([A-Z][A-Z0-9_]{3,})\s*[:=]", text, re.MULTILINE):
                env_vars.add(match.group(1))
    return {
        "config_files": sorted(set(config_files))[:15],
        "env_files": sorted(set(env_files))[:10],
        "env_vars": sorted(env_vars)[:25],
    }


def shape_of(root, files):
    """What kind of software this is."""
    shape = []
    joined = " ".join(files)
    if any(f.startswith("src/server") or "/server" in f or f.startswith("server/")
           for f in files):
        shape.append("server")
    if any(f.startswith("frontend") or f.startswith("webui/frontend")
           or "/frontend" in f or f.startswith("client/") for f in files):
        shape.append("web interface")
    if any(f.endswith("index.html") for f in files):
        shape.append("web page")
    if any(f.startswith("docs/") and f.endswith(".html") for f in files):
        shape.append("landing site")
    if any(f.endswith(".desktop") or f.endswith(".spec") for f in files):
        shape.append("desktop application")
    if any(f.startswith("cmd/") or f.endswith("main.go") for f in files):
        shape.append("command line tool")
    if any(f.startswith("mcp") or "/mcp" in f for f in files):
        shape.append("MCP server")
    if any(f.endswith(".xcodeproj") or "electron" in joined for f in files):
        shape.append("desktop application")
    if any(f.endswith(".app") or "py2app" in joined for f in files):
        shape.append("desktop application")
    if not shape:
        shape.append("library or script")
    return sorted(set(shape))


def existing_readme(root):
    """What the README already says. The facts the owner has written are
    facts."""
    text = read(os.path.join(root, "README.md"))
    if not text:
        return {}
    lines = [l.strip() for l in text.split("\n")]
    heading = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), "")
    paragraphs = []
    current = []
    for line in lines:
        if line.startswith("#"):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return {
        "title": heading,
        "first_paragraphs": [p for p in paragraphs if p][:3],
        "lines": len(text.split("\n")),
        "words": len(text.split()),
    }


def license_of(root):
    text = read(os.path.join(root, "LICENSE"), 2000)
    match = re.search(r"MIT License|Copyright \(c\) (\d{4})", text)
    if match:
        return "MIT"
    if "Apache License" in text:
        return "Apache-2.0"
    if "GNU GENERAL PUBLIC LICENSE" in text:
        return "GPL"
    return None


def ci_of(root):
    """The workflows, and the commands they run."""
    workflows = []
    ci_dir = os.path.join(root, ".github", "workflows")
    if os.path.isdir(ci_dir):
        for name in sorted(os.listdir(ci_dir)):
            if name.endswith((".yml", ".yaml")):
                text = read(os.path.join(ci_dir, name))
                runs = re.findall(r"run:\s*[>|]?\s*(.+)", text)
                workflows.append({
                    "name": name,
                    "runs": [r.strip().strip("'\"") for r in runs][:6],
                })
    return workflows


def tests_of(root, files):
    count = 0
    directories = set()
    for path in files:
        if re.search(r"(^|/)(test_|.*_test\.|.*\.test\.|.*_spec\.)", path):
            count += 1
            directories.add(path.split("/")[0] if "/" in path else ".")
    return {"files": count, "roots": sorted(directories)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="analyze")
    parser.add_argument("repository")
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--out")
    parser.add_argument("--keep", help="leave the clone here")
    args = parser.parse_args(argv)

    work = args.keep or tempfile.mkdtemp(prefix="analyze-")
    target = os.path.join(work, "repo")
    if not os.path.isdir(target):
        run(["git", "clone", "--depth=1", "--quiet",
             "https://github.com/%s/%s.git" % (args.owner, args.repository), target])
    if not os.path.isdir(target):
        sys.stderr.write("analyze: cannot clone %s\n" % args.repository)
        return 2

    files = [f for f in tree_of(target) if not f.endswith("/")]
    meta = run(["git", "-C", target, "log", "-1", "--format=%s|%b"], check=False)

    facts = {
        "repository": args.repository,
        "url": "https://github.com/%s/%s" % (args.owner, args.repository),
        "files": files,
        "tree": tree_of(target),
        "language": language_of(target, files),
        "entry_points": entry_points(target, files),
        "configuration": configuration(target, files),
        "shape": shape_of(target, files),
        "readme": existing_readme(target),
        "license": license_of(target),
        "ci": ci_of(target),
        "tests": tests_of(target, files),
        "manifests": [m for m in MANIFESTS if m in files],
        "run_files": [f for f in RUN_FILES if f in files],
        "last_commit": meta.strip().split("\n")[0] if meta else "",
    }

    if args.out:
        with open(args.out, "w") as handle:
            json.dump(facts, handle, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(facts, indent=2, ensure_ascii=False))

    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
