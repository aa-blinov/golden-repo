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

## Security

These are the findings to look at first.

| Repository | What happens |
| --- | --- |
| `stt-yandex` | `verify=False` on every `requests` call to Speech-to-Text, with `urllib3.disable_warnings` to hide it. The API key and the recording travel over an unverified connection. |
| `alert-bot` | An empty webhook secret disables the check, and the admin API's default token is `change-me-in-production`. The admin API compares with `!=` and answers 200 to the default token. |
| `gchat-sentry-notifier` | `traces_sample_rate=1.0` and `profiles_sample_rate=1.0` send the service's own telemetry to the DSN in full. |
| `gchat-sentry-notifier` | The key is read at import time and a missing one raises `ValueError` there, so the service dies at startup rather than answering. |
| `better-ssh` | The password is written back in plaintext when the SSH key is gone: `save_servers` swallows the `RuntimeError` and then saves. |
| `wiki-js` | The wiki's pages carry no credentials, but the metadata header is written by the instance, so an edit to it is overwritten on the next sync. |
| `anki-bot` | The OpenRouter call blocks the event loop, and the quiz session lives in a dict that intercepts every message from the user until the quiz ends. |
| `petzy` | The rate limits are ten wrong passwords a minute per address, and ten inside fifteen minutes lock that login for fifteen minutes. |
| `rag` | Two live API keys are committed in the notebooks: a Google GenAI key and an OpenRouter key. Both are in the git history and need rotating. |
| `flash-bar-delivery` | The Gemini key is inlined into the client bundle by `define` in `vite.config.ts`, so a published build publishes the key. |
| `the-cuba-times-tgif` | The same, through the same `define` in `vite.config.ts`. |
| `docs` | The webhook handler in `billing.md` never verifies the Stripe signature: `construct_from` parses the body and nothing else, and the `SignatureVerificationError` branch is dead code. Anyone who can POST to the endpoint can forge `invoice.paid`. |
| `cbr-currency-bot` | The `httpx.TimeoutException` clause in `app/api/cbr.py` is unreachable, because `TimeoutException` subclasses `RequestError` and the broader clause comes first. |

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
| `alert-bot` | The access-token check compares a naive SQLite timestamp with an aware one, so every message raises `TypeError` and the webhook answers 500. |
| `alert-bot` | The callback URL is registered as `http://…` even behind TLS termination, because uvicorn runs without `--proxy-headers`. |
| `simple-scripts-collection` | `simple-dns-lookup.py` claims NS, TXT and CNAME lookups; `--type` accepts only A, AAAA, MX, PTR and ALL. |
| `simple-scripts-collection` | `simple-password-generator.py` claims a guaranteed mix of character types; it samples from the union and can return a password with no digit. |
| `qazaq-anki` | `server/server.js` and `server/db.js` are stale copies that nothing runs. The live API is at the repository root. |
| `qazaq-anki` | `docker compose up` fails on the backup service until `secrets/admin_token.txt` exists. |
| `haven` | `.gitignore` carries a stray UTF-16 fragment, which makes the checker read the file as binary. |
| `my-blog` | `docs/layout-system.md` describes classes the current pages do not use. |
| `blog` | `docs/layout-system.md` contradicts the current markup, and two version dialogs are imported nowhere. |
| `roma-stt` | `ConfigStore.Save` drops the configuration keys `AppConfig` does not declare. |
| `MediaSquash` | The queue deadlocks after the first batch: the lock is held across the run and taken again in the `finally`, and `asyncio.Lock` is not reentrant. |
| `MediaSquash` | The GPU rewrite runs on every video command with no NVENC check, so on a machine without an NVIDIA card FFmpeg refuses the command and every video job fails. |
| `MediaSquash` | A cancelled job is recorded as failed, because the terminated process raises into the generic `except`. |
| `simple-rag` | The indexing button raises `KeyError: 'file'` on the first selected row: the grid's columns were renamed and the code was not. |
| `simple-rag` | Hybrid search only works in the run that builds the index, because the docstore is empty when the index is loaded from Chroma. |
| `llm-code-review` | `pyproject.toml` sets `package = false`, so the console script the old README documents is never installed and the documented command fails. |
| `llm-code-review` | Every error path exits 0, so a failed review and an empty one look the same to a pipeline. |
| `llm-code-review` | A bad API key produces a report that says nothing was found. |
| `cli_calendar` | The response body is parsed before the status code is checked, so a non-JSON body escapes the error handler and the CLI prints a traceback. |
| `cli_calendar` | The process environment is ignored: the configuration comes from the `.env` file only. |
| `photo-checker` | The exit code is 0 for a failed validation, and the model-download notice goes to stdout in front of the JSON, so piping to `jq` breaks. |
| `crypto-service` | The exchange endpoint was retired, so both routes answer 503; the parser also never matched the provider's response shape. |
| `the-cuba-times-tgif` | The application never mounts: `index.html` has no entry point, and a syntax error in a component is masked by that. |
| `demo-platform` | The Markdown bold never reaches the PDF: the parser hands `**text**` to ReportLab, whose markup is `<b>`. 179 spans print literally. |
| `roma-stt` | The C# tray rewrites `config.yaml` on every start, with the hotkey it managed to register rather than the one that was asked for. |
| `gunicorn-stats` | `GUNICORN_WORKERS` defaults to 4 and `GUNICORN_THREADS` to 1; the old table said 2 and 4. |
| `gunicorn-stats` | The Python floor is 3.8, not 3.6, and `setup-python36.sh` installs Flask 2.3.3 into a 3.6 environment, so pip refuses. |
| `gunicorn-stats` | The systemd unit sets `HTTP_HOST=0.0.0.0` while the services README says the page is localhost-only. |
| `all-about-all` | The per-agent token limits never reach the API: the code passes `max_output_tokens` and the locked pydantic-ai reads `max_tokens`. |
| `all-about-all` | `HTTP_TIMEOUT_SECONDS` and `MAX_CONCURRENT_REQUESTS` are read and ignored; the pipeline is sequential. |
| `all-about-all` | A critique that lists any weakness triggers a second writer call even when the verdict is `approve`. |
| `titles-forecating` | `requirements.txt` is behind `pyproject.toml`, so `import scraper` fails after installing it. |
| `titles-forecating` | Two test files import functions that `scraper.py` replaced, and both raise `ImportError` before a line runs. |
| `titles-forecating` | `save_raw` opens the raw CSV in mode `w`, so every scrape replaces the corpus. |
| `titles-forecating` | A missing API key makes `semantic_similarity` return `0.0`, so an unmeasured metric reaches the report as a score of zero. |
| `anki-bot` | There is no spaced repetition: two statuses, no interval, no due date, no scheduling. |
| `anki-bot` | The card is written to MongoDB before the user confirms it, and cancelling leaves it there. |
| `anki-bot` | `make test` fails without three environment variables, because the settings are built at import time. |
| `metronome` | `expo-asset` is imported but not in `package.json`; it resolves only because it is nested under `expo`. |
| `metronome` | The app declares the microphone permissions and the iOS background audio mode, and uses neither. |
| `self-hosted-search-agent` | The `[N]` citation numbers are positional, and sorting inside `intelligence.py` repoints every citation. |
| `self-hosted-search-agent` | The report always holds exactly one synthetic claim, so the CLI's "Claims (1)" is not a decomposition. |
| `spin-game` | The save keeps the spin summary but not its lines, and `save_run()` does nothing during a spin. |
| `wiki-js` | Twenty-one pages exist twice, as `.md` and `.html`, and the Markdown file is always the newer one. |

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
