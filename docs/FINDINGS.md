# Findings

What the rewrite found in the repositories themselves.

Writing the documents from the code, rather than from the old README, turned
up a fair number of places where the documentation and the code disagreed, and
a few where the code was plainly broken. The agents checked these by running
the code, not by reading it, so the list is a set of reproduced facts rather
than a set of suspicions.

Nothing here was changed. The rule the documents follow is that the code is
the truth, and the code was not touched.

## The documentation was wrong

| Repository | What the documentation said | What the code does |
| --- | --- | --- |
| `cast` | 20 built-in personas | 7 |
| `cast` | A "Hashline LRU Cache" with 20 entries and a sha1 per line | No such cache. There is a fixed list of nine parallel-safe tool names. |
| `cast` | `read` and `grep` run concurrently | `read` is not on the parallel-safe list, so it runs in call order. |
| `cast` | The doom-loop detector fires on 3 consecutive calls | A threshold of 3 inside a sliding window of 12, with `bash_output` exempt. |
| `cast` | The default reply reserve is 8,192 tokens | `settings.ts` clamps it to 32,000. |
| `cast` | `/plugin` is a command | It exists nowhere in `src/`. |
| `project-setup-tool` | 18 project profiles | 20. |
| `project-setup-tool` | 113 tests | 129, and they pass. |
| `project-setup-tool` | `run.sh` takes `--name`, `--profile`, `--dir` | The CLI takes them positionally and has no `--dir`. |
| `lazy-to-text` | The default model is `parakeet-tdt-v3` | `gigaam-v3-ctc`. |
| `lazy-to-text` | The macOS bundle uses the in-process `RegistryBackend` | It spawns a worker and falls back to the in-process backend only if the worker fails. |
| `lazy-to-text` | The overlay sits at `NSScreenSaverWindowLevel` | `NSStatusWindowLevel`. |
| `lazy-to-text` | `setup.py` sets `LSUIElement` | It deliberately does not; the activation policy is switched at runtime. |
| `lazy-to-text` | 670 tests pass | 1,485 pass and 10 are skipped. |
| `lazy-to-text` | The landing page calls the product Windows-only | It says Windows and macOS. |
| `vibe-vpn` | Requires Go 1.21+ | `go.mod` requires 1.25.0 with toolchain go1.26.6. |
| `qazaq-anki` | 30 tools | 31. |
| `qazaq-anki` | The DXT build needs a system `zip` | It zips with the `archiver` package. |
| `templates-mcp` | The build needs a system `zip` binary | Same. |
| `protokol` | 171 passing unit tests | 361 test functions in 21 files. |
| `protokol` | The models are about 0.9 GB | 696 MiB measured. |
| `cronator` | The default login is `admin` / `admin` | Both the password and the secret key are required, and the placeholder is refused at startup. |
| `cronator` | 800+ tests | 86 test files and 688 test functions. |
| `my-blog` | The search state goes into the URL | It is in session storage only. |
| `my-blog` | Mermaid is loaded from a CDN | It is imported from the npm package. |
| `anki-service` | The schema comes from Alembic | `Base.metadata.create_all`; the `alembic_version` table of the checked-in database is empty. |
| `roma-stt` | The two branches share the model path | The Python branch refuses `models/en/ggml-base.bin` and the C# one refuses `ggml-base.en.bin`. |
| `whisper-bot` | The OpenRouter address, the prompt and the Redis host are environment variables | They are constants. |
| `codex-gateway` | `CODEX_CHAT_WRAPPER_MODELS` overrides the config discovery | It prepends to what the file holds. |
| `haven` | The theme count is 25 | The sidebar has 28 buttons. |

## The code is broken

Each of these was reproduced by running it.

| Repository | What happens |
| --- | --- |
| `bitrix-mcp` | `python __main__.py` raises `ValueError: a coroutine was expected, got None`. The module wraps a synchronous `main()` in `asyncio.run()`. |
| `bitrix-mcp` | Both HTTP transports raise `TypeError: FastMCP.run() got an unexpected keyword argument 'port'`. Only stdio starts. |
| `bitrix-mcp` | `requirements.txt` asks for `mcp>=1.0.0`, which installs mcp 2.x, where every test file fails at collection. The ceiling has to be `mcp<2`. |
| `bitrix-mcp` | `MCP_TRANSPORT`, `MCP_PORT`, `MCP_HOST` and `MCP_LOG_LEVEL` are read into the config and then ignored. |
| `bitrix-mcp` | `get_task_fields` is registered and raises `AttributeError`, because `TaskTools` has no such method. |
| `bitrix-mcp` | `mypy.ini` sets `ignore_errors = True` for the three modules that hold the real code. Without those lines, mypy reports 23 errors. |
| `bitrix-mcp` | Every step of `code-quality.yml` carries `continue-on-error: true`, and ruff reports 173 findings. |
| `gchat-sentry-notifier` | The service `Dockerfile` copies only `requirements.txt`, so the image holds no code, and with no `CMD` it inherits the base image's `CMD ["python3"]` and exits. The old README's Docker instructions do not work. |
| `gchat-sentry-notifier` | The error path for a failed call to Google Chat falls through to an unbound `response`, so it ends as an `UnboundLocalError` and a 500. |
| `gchat-sentry-notifier` | The environment filter lowercases the payload's environment but not the allowed list, so `Production` never matches. |
| `coop-watcher` | The `?room=` auto-join emits a bare string while the server destructures `{ roomId, password }`, so the client lands in a room named `undefined` and becomes its host. The Invite button copies that link. |
| `coop-watcher` | The socket effect closes over the first render, so the reconnect branch never re-joins the room. |
| `coop-watcher` | `VKPlayer` has no `setVolume`, so the volume slider changes the number and not the sound. |
| `vibe-vpn` | `Dockerfile.server` builds `./cmd/vibe-vpn`, and the package is `./cmd/vpn`, so the server image does not build. |
| `vibe-vpn` | The generated client's UDP fallback points at port 443 while the generated server listens on 4433. |
| `codex-gateway` | `Makefile` sets `-X main.version=$(VERSION)`, and there is no `version` variable in `main.go`, so the linker ignores it and the binary reports no version. |
| `codex-gateway` | `main_test.go` is not gofmt-clean, so a formatting check in CI fails on that file alone. |
| `self-hosted-search-agent` | `CLAUDE.md` describes a pipeline that is not in the tree: `application/use_cases.py`, `application/legacy_steps.py` and `infrastructure/wikipedia_api.py` are all gone. The orchestrator is `application/unified_runner.py`. |
| `simple-scripts-collection` | `simple-dns-lookup.py` claims NS, TXT and CNAME lookups; `--type` accepts only A, AAAA, MX, PTR and ALL. |
| `simple-scripts-collection` | `simple-password-generator.py` claims a guaranteed mix of character types; it samples from the union and can return a password with no digit. |
| `qazaq-anki` | `server/server.js` and `server/db.js` are stale copies that nothing runs. The live API is at the repository root. |
| `qazaq-anki` | `docker compose up` fails on the backup service until `secrets/admin_token.txt` exists. |
| `haven` | `.gitignore` carries a stray UTF-16 fragment, which makes the checker read the file as binary. |
| `my-blog` | `docs/layout-system.md` describes classes the current pages do not use. |
| `blog` | `docs/layout-system.md` contradicts the current markup, and two version dialogs are imported nowhere. |
| `roma-stt` | `ConfigStore.Save` drops the configuration keys `AppConfig` does not declare. |
| `roma-stt` | The C# tray rewrites `config.yaml` on every start, with the hotkey it managed to register rather than the one that was asked for. |

## What the code cannot say

Several repositories have no licence file, and the house standard says MIT.
Where the agent added one, it added the standard's own text and said so. Two
repositories disagree with the standard on purpose:

- `my-blog` carries "All Rights Reserved" and `UNLICENSED` in its
  `package.json`. The documents say that, and the licence file was left
  alone. Relicensing is the owner's call.
- `ponytail-minimax` carries upstream's copyright, because the six skills are
  byte-identical to an upstream tag.

Several repositories have no description on GitHub, no stars and no
downloads, so there is no audience to describe and no number to quote. The
product records say so rather than inventing one.
