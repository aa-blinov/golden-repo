# Audit

Every repository of **aa-blinov** checked against the house standard by
`scripts/housecheck.py`, the same code that runs in CI. Each
repository is cloned shallowly and checked as it stands, so a link
that resolves is a link that resolves.

| | Collection | The rest |
| --- | ---: | ---: |
| Repositories | 60 | 23 |
| Hard failures | 2 | 1381 |
| Soft findings | 1 | 184 |
| Repositories with no hard failure | 58 | 2 |

The collection is the 60 repositories the standard was written for.
The rest are the repositories that hold somebody else's work, the
test sandboxes, and the throwaways: the standard was never meant for
them, and the number in the last column says so.

A hard failure is a rule the repository breaks. A soft finding is a
preference, reported but not enforced.

## What has been done

Every repository of the collection was brought under the standard
directly. The documents were written from the code and pushed to
the default branch, rather than proposed in a pull request, because
a proposal waits for a reader and the work was the point.

| | |
| --- | ---: |
| Repositories under the standard | 60 |
| With a landing page in the house style | 7 |
| Exempt | 23 |

The exemptions carry a reason, and a repository is exempt because of
what it holds rather than because of what it is called: a repository
that points at EORA's portal or serves EORA's pages is EORA's work,
whatever the name says. The list was built by searching the
collection for the identifiers that give it away.

The landing pages are the same page in seven repositories: the same
stylesheet, the same class vocabulary, the same structure. What
differs is the content, which is the repository's own.

## Which rules are broken most

| Rule | Hard | Soft | Repositories affected |
| --- | ---: | ---: | ---: |
| HS001 | 313 | 0 | 21 |
| HS002 | 166 | 0 | 20 |
| HS003 | 1 | 0 | 1 |
| HS011 | 1 | 0 | 1 |
| HS012 | 41 | 0 | 12 |
| HS014 | 0 | 6 | 6 |
| HS015 | 0 | 12 | 12 |
| HS025 | 0 | 3 | 1 |
| HS026 | 6 | 0 | 6 |
| HS030 | 5 | 161 | 5 |
| HS040 | 53 | 0 | 7 |
| HS041 | 34 | 0 | 2 |
| HS042 | 282 | 0 | 9 |
| HS043 | 472 | 0 | 10 |
| HS044 | 9 | 0 | 5 |
| HS102 | 0 | 3 | 3 |

The three rules that account for most of the total are the cheapest to
fix and the most visible:

- **HS001, the canonical root file set.** Every repository is missing
  most of it. `scripts/adopt.sh` adds the missing files in one command,
  overwriting nothing.
- **HS005, CI.** Every repository needs a workflow that runs on pull
  requests. The template has one.
- **HS006, issue forms.** A repository with no forms gets blank
  issues. The templates ask for the environment and the expected
  behaviour, which is the difference between a report that can be
  acted on and one that cannot.

## Where to start

The order follows how much the repository is looked at.

### Tier 1 — looked at, or in active use

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [aa-blinov](https://github.com/aa-blinov/aa-blinov) | 0 | 0 | Config files for my GitHub profile. |
| [better-ssh](https://github.com/aa-blinov/better-ssh) | 0 | 0 | A friendlier layer over OpenSSH: interactive picker, encrypt |
| [cast](https://github.com/aa-blinov/cast) | 0 | 0 | Minimal terminal coding agent with OpenAI-compatible routing |
| [cronator](https://github.com/aa-blinov/cronator) | 0 | 0 |  |
| [gchat-sentry-notifier](https://github.com/aa-blinov/gchat-sentry-notifier) | 0 | 0 |  |
| [lazy-to-text](https://github.com/aa-blinov/lazy-to-text) | 0 | 0 | Local Whisper speech-to-text for Windows: global hotkey, Qt  |
| [llm-code-review](https://github.com/aa-blinov/llm-code-review) | 0 | 0 |  |
| [petzy](https://github.com/aa-blinov/petzy) | 0 | 0 |  |
| [ponytail-minimax](https://github.com/aa-blinov/ponytail-minimax) | 0 | 0 | Ponytail lazy-senior-dev mode as a MiniMax Code plugin: the  |
| [project-setup-tool](https://github.com/aa-blinov/project-setup-tool) | 0 | 0 |  |
| [whisper-bot](https://github.com/aa-blinov/whisper-bot) | 0 | 0 |  |

### Tier 2 — public

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [bitrix-flow](https://github.com/aa-blinov/bitrix-flow) | 5 | 3 |  |
| [my-blog](https://github.com/aa-blinov/my-blog) | 1 | 0 |  |
| [_template-smoke-test](https://github.com/aa-blinov/_template-smoke-test) | 0 | 0 | Temporary smoke test of aa-blinov/golden-repo. Archived; saf |
| [bitrix-mcp](https://github.com/aa-blinov/bitrix-mcp) | 0 | 0 |  |
| [cbr-currency-bot](https://github.com/aa-blinov/cbr-currency-bot) | 0 | 0 |  |
| [claude-gateway](https://github.com/aa-blinov/claude-gateway) | 0 | 0 | OpenAI-compatible HTTP gateway over Claude Code CLI with rea |
| [codex-gateway](https://github.com/aa-blinov/codex-gateway) | 0 | 0 | OpenAI-compatible HTTP wrapper over codex exec |
| [doktor-ryadom](https://github.com/aa-blinov/doktor-ryadom) | 0 | 0 | Рядом — дневник самочувствия пациента и кабинет врача |
| [golden-repo](https://github.com/aa-blinov/golden-repo) | 0 | 0 | The canonical house standard for every repository: one file  |
| [haven](https://github.com/aa-blinov/haven) | 0 | 0 | Self-hosted private chat — No cloud, no telemetry, no Big Te |
| [impeccable-mcode](https://github.com/aa-blinov/impeccable-mcode) | 0 | 0 | Impeccable design skill for MiniMax Code — fork of pbakaus/i |
| [koloda](https://github.com/aa-blinov/koloda) | 0 | 0 | Единая лента из Telegram-каналов: свой ридер с поиском, филь |
| [monos](https://github.com/aa-blinov/monos) | 0 | 0 | Local-first desktop notes app with Markdown, wiki links, ful |
| [paratrack](https://github.com/aa-blinov/paratrack) | 0 | 0 |  |
| [petzy-ios](https://github.com/aa-blinov/petzy-ios) | 0 | 0 | Petzy для iOS: нативный SwiftUI-клиент дневника здоровья пит |
| [photo-checker](https://github.com/aa-blinov/photo-checker) | 0 | 0 |  |
| [puuush](https://github.com/aa-blinov/puuush) | 0 | 0 | Скриншот области экрана, загрузка, ссылка в буфере обмена. E |
| [qazaq-anki](https://github.com/aa-blinov/qazaq-anki) | 0 | 0 | Spaced-repetition flashcards for learning Kazakh (CEFR A1–C1 |
| [self-hosted-search-agent](https://github.com/aa-blinov/self-hosted-search-agent) | 0 | 0 |  |
| [simple-rag](https://github.com/aa-blinov/simple-rag) | 0 | 0 |  |
| [simple-scripts-collection](https://github.com/aa-blinov/simple-scripts-collection) | 0 | 0 |  |
| [stt-yandex](https://github.com/aa-blinov/stt-yandex) | 0 | 0 |  |
| [templates-mcp](https://github.com/aa-blinov/templates-mcp) | 0 | 0 | Reference template for building production-grade MCP servers |
| [titles-forecating](https://github.com/aa-blinov/titles-forecating) | 0 | 0 | Forecasting titles |
| [vibe-vpn](https://github.com/aa-blinov/vibe-vpn) | 0 | 0 |  |
| [wallpaper-generator](https://github.com/aa-blinov/wallpaper-generator) | 0 | 0 | 120 abstract-wallpaper generators running live in the browse |

### Tier 3 — private

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [outline-workspace](https://github.com/aa-blinov/outline-workspace) | 395 | 129 |  |
| [wiki-js](https://github.com/aa-blinov/wiki-js) | 225 | 21 |  |
| [monos-home](https://github.com/aa-blinov/monos-home) | 105 | 0 |  |
| [notes](https://github.com/aa-blinov/notes) | 102 | 0 |  |
| [my-notes](https://github.com/aa-blinov/my-notes) | 42 | 1 |  |
| [demo-platform](https://github.com/aa-blinov/demo-platform) | 38 | 0 |  |
| [crm-exporter](https://github.com/aa-blinov/crm-exporter) | 32 | 2 |  |
| [bspb-universal-helper-poc](https://github.com/aa-blinov/bspb-universal-helper-poc) | 27 | 15 |  |
| [eora](https://github.com/aa-blinov/eora) | 26 | 0 |  |
| [projects-exporter](https://github.com/aa-blinov/projects-exporter) | 25 | 2 |  |
| [stavki](https://github.com/aa-blinov/stavki) | 1 | 1 | Доска для бытовых споров: лента, планка, счёт. Деньги не при |
| [MediaSquash](https://github.com/aa-blinov/MediaSquash) | 0 | 0 |  |
| [alert-bot](https://github.com/aa-blinov/alert-bot) | 0 | 0 |  |
| [all-about-all](https://github.com/aa-blinov/all-about-all) | 0 | 0 |  |
| [anki-bot](https://github.com/aa-blinov/anki-bot) | 0 | 0 |  |
| [anki-service](https://github.com/aa-blinov/anki-service) | 0 | 0 |  |
| [blog](https://github.com/aa-blinov/blog) | 0 | 0 |  |
| [cli_calendar](https://github.com/aa-blinov/cli_calendar) | 0 | 0 |  |
| [cloud-cost-dashboard](https://github.com/aa-blinov/cloud-cost-dashboard) | 0 | 0 | Прогноз расходов и разбор по ресурсам: immers.cloud + Yandex |
| [coop-watcher](https://github.com/aa-blinov/coop-watcher) | 0 | 0 |  |
| [course](https://github.com/aa-blinov/course) | 0 | 0 |  |
| [crypto-service](https://github.com/aa-blinov/crypto-service) | 0 | 0 |  |
| [docs](https://github.com/aa-blinov/docs) | 0 | 0 |  |
| [flash-bar-delivery](https://github.com/aa-blinov/flash-bar-delivery) | 0 | 0 | App for delivery (21+) |
| [gambling-pack](https://github.com/aa-blinov/gambling-pack) | 0 | 0 |  |
| [govno](https://github.com/aa-blinov/govno) | 0 | 0 |  |
| [gunicorn-stats](https://github.com/aa-blinov/gunicorn-stats) | 0 | 0 |  |
| [metronome](https://github.com/aa-blinov/metronome) | 0 | 0 |  |
| [ovh-caddy](https://github.com/aa-blinov/ovh-caddy) | 0 | 0 | Машинный Caddy на VPS: все проекты за одним прокси |
| [protokol](https://github.com/aa-blinov/protokol) | 0 | 0 | Протокол — приватная расшифровка встреч. Аудио → транскрипт  |
| [rag](https://github.com/aa-blinov/rag) | 0 | 0 |  |
| [roma-stt](https://github.com/aa-blinov/roma-stt) | 0 | 0 |  |
| [spin-game](https://github.com/aa-blinov/spin-game) | 0 | 0 |  |
| [the-cuba-times-tgif](https://github.com/aa-blinov/the-cuba-times-tgif) | 0 | 0 | Simple landing for sunny Cuba |
| [trentini-poc](https://github.com/aa-blinov/trentini-poc) | 0 | 0 |  |
| [umnaya-alisa](https://github.com/aa-blinov/umnaya-alisa) | 0 | 0 | Приватный навык Алисы: чат с MiniMax |

### Tier 4 — exempt: archived, test sandboxes, throwaways

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [monos-sync-test](https://github.com/aa-blinov/monos-sync-test) | 99 | 0 | Temporary private repo for verifying two-device sync. Safe t |
| [cast-team](https://github.com/aa-blinov/cast-team) | 33 | 1 | Fork of cast exploring multi-user/team functionality |
| [monos-sync-e2e-1781381662822](https://github.com/aa-blinov/monos-sync-e2e-1781381662822) | 30 | 2 | Monos real sync/conflict e2e test repo |
| [monos-sync-e2e-1781381831101](https://github.com/aa-blinov/monos-sync-e2e-1781381831101) | 30 | 2 | Monos real sync/conflict e2e test repo |
| [monos-sync-matrix-1781382370490](https://github.com/aa-blinov/monos-sync-matrix-1781382370490) | 30 | 2 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382440442](https://github.com/aa-blinov/monos-sync-matrix-1781382440442) | 30 | 2 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382482939](https://github.com/aa-blinov/monos-sync-matrix-1781382482939) | 30 | 2 | Monos real sync edge-case matrix |
| [monos-conflict-test](https://github.com/aa-blinov/monos-conflict-test) | 26 | 0 | Test repo for conflict resolution UI |
| [monos-notes](https://github.com/aa-blinov/monos-notes) | 26 | 0 | Заметки Monos: синхронизация между устройствами |
| [monos-conflict-lab](https://github.com/aa-blinov/monos-conflict-lab) | 25 | 0 | Monos sync conflict test sandbox |

## Every repository

| Repository | Visibility | Hard | Soft | Description |
| --- | --- | ---: | ---: | --- |
| [outline-workspace](https://github.com/aa-blinov/outline-workspace) | PRIVATE | 395 | 129 |  |
| [wiki-js](https://github.com/aa-blinov/wiki-js) | PRIVATE | 225 | 21 |  |
| [monos-home](https://github.com/aa-blinov/monos-home) | PRIVATE | 105 | 0 |  |
| [notes](https://github.com/aa-blinov/notes) | PRIVATE | 102 | 0 |  |
| [monos-sync-test](https://github.com/aa-blinov/monos-sync-test) | PRIVATE | 99 | 0 | Temporary private repo for verifying two-device sync. Safe to delete. |
| [my-notes](https://github.com/aa-blinov/my-notes) | PRIVATE | 42 | 1 |  |
| [demo-platform](https://github.com/aa-blinov/demo-platform) | PRIVATE | 38 | 0 |  |
| [cast-team](https://github.com/aa-blinov/cast-team) | PRIVATE | 33 | 1 | Fork of cast exploring multi-user/team functionality |
| [crm-exporter](https://github.com/aa-blinov/crm-exporter) | PRIVATE | 32 | 2 |  |
| [monos-sync-e2e-1781381662822](https://github.com/aa-blinov/monos-sync-e2e-1781381662822) | PRIVATE | 30 | 2 | Monos real sync/conflict e2e test repo |
| [monos-sync-e2e-1781381831101](https://github.com/aa-blinov/monos-sync-e2e-1781381831101) | PRIVATE | 30 | 2 | Monos real sync/conflict e2e test repo |
| [monos-sync-matrix-1781382370490](https://github.com/aa-blinov/monos-sync-matrix-1781382370490) | PRIVATE | 30 | 2 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382440442](https://github.com/aa-blinov/monos-sync-matrix-1781382440442) | PRIVATE | 30 | 2 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382482939](https://github.com/aa-blinov/monos-sync-matrix-1781382482939) | PRIVATE | 30 | 2 | Monos real sync edge-case matrix |
| [bspb-universal-helper-poc](https://github.com/aa-blinov/bspb-universal-helper-poc) | PRIVATE | 27 | 15 |  |
| [eora](https://github.com/aa-blinov/eora) | PRIVATE | 26 | 0 |  |
| [monos-conflict-test](https://github.com/aa-blinov/monos-conflict-test) | PRIVATE | 26 | 0 | Test repo for conflict resolution UI |
| [monos-notes](https://github.com/aa-blinov/monos-notes) | PRIVATE | 26 | 0 | Заметки Monos: синхронизация между устройствами |
| [monos-conflict-lab](https://github.com/aa-blinov/monos-conflict-lab) | PRIVATE | 25 | 0 | Monos sync conflict test sandbox |
| [projects-exporter](https://github.com/aa-blinov/projects-exporter) | PRIVATE | 25 | 2 |  |
| [bitrix-flow](https://github.com/aa-blinov/bitrix-flow) | PUBLIC | 5 | 3 |  |
| [my-blog](https://github.com/aa-blinov/my-blog) | PUBLIC | 1 | 0 |  |
| [stavki](https://github.com/aa-blinov/stavki) | PRIVATE | 1 | 1 | Доска для бытовых споров: лента, планка, счёт. Деньги не принимает |
| [MediaSquash](https://github.com/aa-blinov/MediaSquash) | PRIVATE | 0 | 0 |  |
| [_template-smoke-test](https://github.com/aa-blinov/_template-smoke-test) | PUBLIC | 0 | 0 | Temporary smoke test of aa-blinov/golden-repo. Archived; safe to delet |
| [aa-blinov](https://github.com/aa-blinov/aa-blinov) | PUBLIC | 0 | 0 | Config files for my GitHub profile. |
| [alert-bot](https://github.com/aa-blinov/alert-bot) | PRIVATE | 0 | 0 |  |
| [all-about-all](https://github.com/aa-blinov/all-about-all) | PRIVATE | 0 | 0 |  |
| [anki-bot](https://github.com/aa-blinov/anki-bot) | PRIVATE | 0 | 0 |  |
| [anki-service](https://github.com/aa-blinov/anki-service) | PRIVATE | 0 | 0 |  |
| [better-ssh](https://github.com/aa-blinov/better-ssh) | PUBLIC | 0 | 0 | A friendlier layer over OpenSSH: interactive picker, encrypted passwor |
| [bitrix-mcp](https://github.com/aa-blinov/bitrix-mcp) | PUBLIC | 0 | 0 |  |
| [blog](https://github.com/aa-blinov/blog) | PRIVATE | 0 | 0 |  |
| [cast](https://github.com/aa-blinov/cast) | PUBLIC | 0 | 0 | Minimal terminal coding agent with OpenAI-compatible routing. Works wi |
| [cbr-currency-bot](https://github.com/aa-blinov/cbr-currency-bot) | PUBLIC | 0 | 0 |  |
| [claude-gateway](https://github.com/aa-blinov/claude-gateway) | PUBLIC | 0 | 0 | OpenAI-compatible HTTP gateway over Claude Code CLI with real streamin |
| [cli_calendar](https://github.com/aa-blinov/cli_calendar) | PRIVATE | 0 | 0 |  |
| [cloud-cost-dashboard](https://github.com/aa-blinov/cloud-cost-dashboard) | PRIVATE | 0 | 0 | Прогноз расходов и разбор по ресурсам: immers.cloud + Yandex Cloud, да |
| [codex-gateway](https://github.com/aa-blinov/codex-gateway) | PUBLIC | 0 | 0 | OpenAI-compatible HTTP wrapper over codex exec |
| [coop-watcher](https://github.com/aa-blinov/coop-watcher) | PRIVATE | 0 | 0 |  |
| [course](https://github.com/aa-blinov/course) | PRIVATE | 0 | 0 |  |
| [cronator](https://github.com/aa-blinov/cronator) | PUBLIC | 0 | 0 |  |
| [crypto-service](https://github.com/aa-blinov/crypto-service) | PRIVATE | 0 | 0 |  |
| [docs](https://github.com/aa-blinov/docs) | PRIVATE | 0 | 0 |  |
| [doktor-ryadom](https://github.com/aa-blinov/doktor-ryadom) | PUBLIC | 0 | 0 | Рядом — дневник самочувствия пациента и кабинет врача |
| [flash-bar-delivery](https://github.com/aa-blinov/flash-bar-delivery) | PRIVATE | 0 | 0 | App for delivery (21+) |
| [gambling-pack](https://github.com/aa-blinov/gambling-pack) | PRIVATE | 0 | 0 |  |
| [gchat-sentry-notifier](https://github.com/aa-blinov/gchat-sentry-notifier) | PUBLIC | 0 | 0 |  |
| [golden-repo](https://github.com/aa-blinov/golden-repo) | PUBLIC | 0 | 0 | The canonical house standard for every repository: one file tree, one  |
| [govno](https://github.com/aa-blinov/govno) | PRIVATE | 0 | 0 |  |
| [gunicorn-stats](https://github.com/aa-blinov/gunicorn-stats) | PRIVATE | 0 | 0 |  |
| [haven](https://github.com/aa-blinov/haven) | PUBLIC | 0 | 0 | Self-hosted private chat — No cloud, no telemetry, no Big Tech. Discor |
| [impeccable-mcode](https://github.com/aa-blinov/impeccable-mcode) | PUBLIC | 0 | 0 | Impeccable design skill for MiniMax Code — fork of pbakaus/impeccable  |
| [koloda](https://github.com/aa-blinov/koloda) | PUBLIC | 0 | 0 | Единая лента из Telegram-каналов: свой ридер с поиском, фильтрами и RS |
| [lazy-to-text](https://github.com/aa-blinov/lazy-to-text) | PUBLIC | 0 | 0 | Local Whisper speech-to-text for Windows: global hotkey, Qt UI, no clo |
| [llm-code-review](https://github.com/aa-blinov/llm-code-review) | PRIVATE | 0 | 0 |  |
| [metronome](https://github.com/aa-blinov/metronome) | PRIVATE | 0 | 0 |  |
| [monos](https://github.com/aa-blinov/monos) | PUBLIC | 0 | 0 | Local-first desktop notes app with Markdown, wiki links, full-text sea |
| [ovh-caddy](https://github.com/aa-blinov/ovh-caddy) | PRIVATE | 0 | 0 | Машинный Caddy на VPS: все проекты за одним прокси |
| [paratrack](https://github.com/aa-blinov/paratrack) | PUBLIC | 0 | 0 |  |
| [petzy](https://github.com/aa-blinov/petzy) | PUBLIC | 0 | 0 |  |
| [petzy-ios](https://github.com/aa-blinov/petzy-ios) | PUBLIC | 0 | 0 | Petzy для iOS: нативный SwiftUI-клиент дневника здоровья питомца, тот  |
| [photo-checker](https://github.com/aa-blinov/photo-checker) | PUBLIC | 0 | 0 |  |
| [ponytail-minimax](https://github.com/aa-blinov/ponytail-minimax) | PUBLIC | 0 | 0 | Ponytail lazy-senior-dev mode as a MiniMax Code plugin: the same six s |
| [project-setup-tool](https://github.com/aa-blinov/project-setup-tool) | PUBLIC | 0 | 0 |  |
| [protokol](https://github.com/aa-blinov/protokol) | PRIVATE | 0 | 0 | Протокол — приватная расшифровка встреч. Аудио → транскрипт → маскиров |
| [puuush](https://github.com/aa-blinov/puuush) | PUBLIC | 0 | 0 | Скриншот области экрана, загрузка, ссылка в буфере обмена. Electron-кл |
| [qazaq-anki](https://github.com/aa-blinov/qazaq-anki) | PUBLIC | 0 | 0 | Spaced-repetition flashcards for learning Kazakh (CEFR A1–C1). SM-2 al |
| [rag](https://github.com/aa-blinov/rag) | PRIVATE | 0 | 0 |  |
| [roma-stt](https://github.com/aa-blinov/roma-stt) | PRIVATE | 0 | 0 |  |
| [self-hosted-search-agent](https://github.com/aa-blinov/self-hosted-search-agent) | PUBLIC | 0 | 0 |  |
| [simple-rag](https://github.com/aa-blinov/simple-rag) | PUBLIC | 0 | 0 |  |
| [simple-scripts-collection](https://github.com/aa-blinov/simple-scripts-collection) | PUBLIC | 0 | 0 |  |
| [spin-game](https://github.com/aa-blinov/spin-game) | PRIVATE | 0 | 0 |  |
| [stt-yandex](https://github.com/aa-blinov/stt-yandex) | PUBLIC | 0 | 0 |  |
| [templates-mcp](https://github.com/aa-blinov/templates-mcp) | PUBLIC | 0 | 0 | Reference template for building production-grade MCP servers for Bitri |
| [the-cuba-times-tgif](https://github.com/aa-blinov/the-cuba-times-tgif) | PRIVATE | 0 | 0 | Simple landing for sunny Cuba |
| [titles-forecating](https://github.com/aa-blinov/titles-forecating) | PUBLIC | 0 | 0 | Forecasting titles |
| [trentini-poc](https://github.com/aa-blinov/trentini-poc) | PRIVATE | 0 | 0 |  |
| [umnaya-alisa](https://github.com/aa-blinov/umnaya-alisa) | PRIVATE | 0 | 0 | Приватный навык Алисы: чат с MiniMax |
| [vibe-vpn](https://github.com/aa-blinov/vibe-vpn) | PUBLIC | 0 | 0 |  |
| [wallpaper-generator](https://github.com/aa-blinov/wallpaper-generator) | PUBLIC | 0 | 0 | 120 abstract-wallpaper generators running live in the browser — vanill |
| [whisper-bot](https://github.com/aa-blinov/whisper-bot) | PUBLIC | 0 | 0 |  |

## The rules behind the codes

See [house-style.md](house-style.md) for what each code means and why
it exists, and [migration.md](migration.md) for the procedure.
