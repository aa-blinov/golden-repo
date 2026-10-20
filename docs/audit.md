# Audit

Every repository of **aa-blinov** checked against the house standard by
`scripts/housecheck.py`, the same code that runs in CI. Each
repository is cloned shallowly and checked as it stands, so a link
that resolves is a link that resolves.

| | |
| --- | --- |
| Repositories checked | 82 |
| Hard failures | 3315 |
| Soft findings | 433 |
| Repositories with no hard failure | 0 |

A hard failure is a rule the repository breaks. A soft finding is a
preference, reported but not enforced.

## What has been done

Every repository in the collection has an open pull request that
adopts the standard. The pull request adds the files and touches
nothing that already existed.

| | |
| --- | ---: |
| Repositories with an adoption pull request | 65 |
| Exempt | 18 |

The exemptions are the standard itself, the test bench, the archived
fork, and the sync sandboxes. A rule that cannot be applied
everywhere is not a rule.

The house-style check on those pull requests is red, and that is the
standard working: `PRODUCT.md` and the other files arrive as
starting points, and the product truth cannot be defaulted. A
repository's own CI stays green, because the pull request changes
nothing that already existed.

## Which rules are broken most

| Rule | Hard | Soft | Repositories affected |
| --- | ---: | ---: | ---: |
| HS001 | 683 | 0 | 81 |
| HS002 | 445 | 0 | 82 |
| HS003 | 1 | 0 | 1 |
| HS005 | 4 | 0 | 4 |
| HS007 | 1 | 0 | 1 |
| HS009 | 0 | 1 | 1 |
| HS011 | 30 | 0 | 30 |
| HS012 | 151 | 0 | 61 |
| HS013 | 0 | 7 | 7 |
| HS014 | 0 | 7 | 7 |
| HS015 | 0 | 56 | 56 |
| HS021 | 9 | 0 | 5 |
| HS022 | 1 | 0 | 1 |
| HS024 | 2 | 0 | 2 |
| HS030 | 48 | 285 | 16 |
| HS031 | 6 | 0 | 5 |
| HS040 | 320 | 0 | 46 |
| HS041 | 35 | 0 | 3 |
| HS042 | 447 | 0 | 40 |
| HS043 | 1120 | 0 | 55 |
| HS044 | 12 | 0 | 8 |
| HS100 | 0 | 56 | 56 |
| HS102 | 0 | 21 | 21 |

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
| [petzy](https://github.com/aa-blinov/petzy) | 95 | 3 |  |
| [cast](https://github.com/aa-blinov/cast) | 70 | 2 | Minimal terminal coding agent with OpenAI-compatible routing |
| [lazy-to-text](https://github.com/aa-blinov/lazy-to-text) | 39 | 1 | Local Whisper speech-to-text for Windows: global hotkey, Qt  |
| [cronator](https://github.com/aa-blinov/cronator) | 31 | 1 |  |
| [gchat-sentry-notifier](https://github.com/aa-blinov/gchat-sentry-notifier) | 27 | 2 |  |
| [llm-code-review](https://github.com/aa-blinov/llm-code-review) | 24 | 2 |  |
| [whisper-bot](https://github.com/aa-blinov/whisper-bot) | 24 | 3 |  |
| [aa-blinov](https://github.com/aa-blinov/aa-blinov) | 22 | 2 | Config files for my GitHub profile. |
| [ponytail-minimax](https://github.com/aa-blinov/ponytail-minimax) | 18 | 1 | Ponytail lazy-senior-dev mode as a MiniMax Code plugin: the  |
| [project-setup-tool](https://github.com/aa-blinov/project-setup-tool) | 16 | 1 |  |
| [better-ssh](https://github.com/aa-blinov/better-ssh) | 11 | 2 | A friendlier layer over OpenSSH: interactive picker, encrypt |

### Tier 2 — public

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [paratrack](https://github.com/aa-blinov/paratrack) | 234 | 4 |  |
| [haven](https://github.com/aa-blinov/haven) | 65 | 1 | Self-hosted private chat — No cloud, no telemetry, no Big Te |
| [monos](https://github.com/aa-blinov/monos) | 57 | 2 | Local-first desktop notes app with Markdown, wiki links, ful |
| [doktor-ryadom](https://github.com/aa-blinov/doktor-ryadom) | 45 | 0 | Рядом — дневник самочувствия пациента и кабинет врача |
| [qazaq-anki](https://github.com/aa-blinov/qazaq-anki) | 41 | 2 | Spaced-repetition flashcards for learning Kazakh (CEFR A1–C1 |
| [my-blog](https://github.com/aa-blinov/my-blog) | 38 | 105 |  |
| [titles-forecating](https://github.com/aa-blinov/titles-forecating) | 35 | 1 | Forecasting titles |
| [impeccable-mcode](https://github.com/aa-blinov/impeccable-mcode) | 31 | 1 | Impeccable design skill for MiniMax Code — fork of pbakaus/i |
| [petzy-ios](https://github.com/aa-blinov/petzy-ios) | 29 | 3 | Petzy для iOS: нативный SwiftUI-клиент дневника здоровья пит |
| [templates-mcp](https://github.com/aa-blinov/templates-mcp) | 29 | 0 | Reference template for building production-grade MCP servers |
| [koloda](https://github.com/aa-blinov/koloda) | 28 | 3 | Единая лента из Telegram-каналов: свой ридер с поиском, филь |
| [puuush](https://github.com/aa-blinov/puuush) | 27 | 2 | Скриншот области экрана, загрузка, ссылка в буфере обмена. E |
| [wallpaper-generator](https://github.com/aa-blinov/wallpaper-generator) | 27 | 3 | 120 abstract-wallpaper generators running live in the browse |
| [cbr-currency-bot](https://github.com/aa-blinov/cbr-currency-bot) | 25 | 2 |  |
| [simple-scripts-collection](https://github.com/aa-blinov/simple-scripts-collection) | 22 | 2 |  |
| [bitrix-mcp](https://github.com/aa-blinov/bitrix-mcp) | 20 | 2 |  |
| [photo-checker](https://github.com/aa-blinov/photo-checker) | 20 | 2 |  |
| [self-hosted-search-agent](https://github.com/aa-blinov/self-hosted-search-agent) | 20 | 1 |  |
| [simple-rag](https://github.com/aa-blinov/simple-rag) | 20 | 1 |  |
| [stt-yandex](https://github.com/aa-blinov/stt-yandex) | 20 | 2 |  |
| [claude-gateway](https://github.com/aa-blinov/claude-gateway) | 19 | 2 | OpenAI-compatible HTTP gateway over Claude Code CLI with rea |
| [codex-gateway](https://github.com/aa-blinov/codex-gateway) | 18 | 2 | OpenAI-compatible HTTP wrapper over codex exec |
| [vibe-vpn](https://github.com/aa-blinov/vibe-vpn) | 18 | 2 |  |
| [bitrix-flow](https://github.com/aa-blinov/bitrix-flow) | 16 | 2 |  |
| [golden-repo](https://github.com/aa-blinov/golden-repo) | 1 | 0 | The canonical house standard for every repository: one file  |

### Tier 3 — private

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [outline-workspace](https://github.com/aa-blinov/outline-workspace) | 402 | 129 |  |
| [wiki-js](https://github.com/aa-blinov/wiki-js) | 219 | 22 |  |
| [monos-home](https://github.com/aa-blinov/monos-home) | 101 | 0 |  |
| [notes](https://github.com/aa-blinov/notes) | 98 | 1 |  |
| [stavki](https://github.com/aa-blinov/stavki) | 73 | 3 | Доска для бытовых споров: лента, планка, счёт. Деньги не при |
| [protokol](https://github.com/aa-blinov/protokol) | 56 | 4 | Протокол — приватная расшифровка встреч. Аудио → транскрипт  |
| [flash-bar-delivery](https://github.com/aa-blinov/flash-bar-delivery) | 48 | 1 | App for delivery (21+) |
| [the-cuba-times-tgif](https://github.com/aa-blinov/the-cuba-times-tgif) | 43 | 1 | Simple landing for sunny Cuba |
| [anki-bot](https://github.com/aa-blinov/anki-bot) | 36 | 3 |  |
| [my-notes](https://github.com/aa-blinov/my-notes) | 35 | 2 |  |
| [gambling-pack](https://github.com/aa-blinov/gambling-pack) | 32 | 2 |  |
| [metronome](https://github.com/aa-blinov/metronome) | 31 | 2 |  |
| [blog](https://github.com/aa-blinov/blog) | 30 | 3 |  |
| [demo-platform](https://github.com/aa-blinov/demo-platform) | 30 | 1 |  |
| [MediaSquash](https://github.com/aa-blinov/MediaSquash) | 28 | 2 |  |
| [umnaya-alisa](https://github.com/aa-blinov/umnaya-alisa) | 28 | 1 | Приватный навык Алисы: чат с MiniMax |
| [anki-service](https://github.com/aa-blinov/anki-service) | 27 | 7 |  |
| [crm-exporter](https://github.com/aa-blinov/crm-exporter) | 25 | 3 |  |
| [docs](https://github.com/aa-blinov/docs) | 25 | 3 |  |
| [gunicorn-stats](https://github.com/aa-blinov/gunicorn-stats) | 25 | 2 |  |
| [rag](https://github.com/aa-blinov/rag) | 25 | 2 |  |
| [alert-bot](https://github.com/aa-blinov/alert-bot) | 24 | 3 |  |
| [cloud-cost-dashboard](https://github.com/aa-blinov/cloud-cost-dashboard) | 24 | 2 | Прогноз расходов и разбор по ресурсам: immers.cloud + Yandex |
| [coop-watcher](https://github.com/aa-blinov/coop-watcher) | 24 | 1 |  |
| [govno](https://github.com/aa-blinov/govno) | 24 | 1 |  |
| [cli_calendar](https://github.com/aa-blinov/cli_calendar) | 22 | 2 |  |
| [crypto-service](https://github.com/aa-blinov/crypto-service) | 22 | 2 |  |
| [all-about-all](https://github.com/aa-blinov/all-about-all) | 20 | 2 |  |
| [bspb-universal-helper-poc](https://github.com/aa-blinov/bspb-universal-helper-poc) | 19 | 15 |  |
| [course](https://github.com/aa-blinov/course) | 19 | 0 |  |
| [projects-exporter](https://github.com/aa-blinov/projects-exporter) | 19 | 2 |  |
| [roma-stt](https://github.com/aa-blinov/roma-stt) | 19 | 2 |  |
| [eora](https://github.com/aa-blinov/eora) | 18 | 1 |  |
| [ovh-caddy](https://github.com/aa-blinov/ovh-caddy) | 18 | 1 | Машинный Caddy на VPS: все проекты за одним прокси |
| [spin-game](https://github.com/aa-blinov/spin-game) | 18 | 1 |  |
| [trentini-poc](https://github.com/aa-blinov/trentini-poc) | 16 | 17 |  |

### Tier 4 — exempt: archived, test sandboxes, throwaways

| Repository | Hard | Soft | Description |
| --- | ---: | ---: | --- |
| [monos-sync-test](https://github.com/aa-blinov/monos-sync-test) | 95 | 0 | Temporary private repo for verifying two-device sync. Safe t |
| [cast-team](https://github.com/aa-blinov/cast-team) | 57 | 2 | Fork of cast exploring multi-user/team functionality |
| [monos-sync-e2e-1781381662822](https://github.com/aa-blinov/monos-sync-e2e-1781381662822) | 21 | 3 | Monos real sync/conflict e2e test repo |
| [monos-sync-e2e-1781381831101](https://github.com/aa-blinov/monos-sync-e2e-1781381831101) | 21 | 3 | Monos real sync/conflict e2e test repo |
| [monos-sync-matrix-1781382370490](https://github.com/aa-blinov/monos-sync-matrix-1781382370490) | 21 | 3 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382440442](https://github.com/aa-blinov/monos-sync-matrix-1781382440442) | 21 | 3 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382482939](https://github.com/aa-blinov/monos-sync-matrix-1781382482939) | 21 | 3 | Monos real sync edge-case matrix |
| [monos-conflict-test](https://github.com/aa-blinov/monos-conflict-test) | 18 | 1 | Test repo for conflict resolution UI |
| [monos-notes](https://github.com/aa-blinov/monos-notes) | 18 | 1 | Заметки Monos: синхронизация между устройствами |
| [monos-conflict-lab](https://github.com/aa-blinov/monos-conflict-lab) | 17 | 1 | Monos sync conflict test sandbox |

## Every repository

| Repository | Visibility | Hard | Soft | Description |
| --- | --- | ---: | ---: | --- |
| [outline-workspace](https://github.com/aa-blinov/outline-workspace) | PRIVATE | 402 | 129 |  |
| [paratrack](https://github.com/aa-blinov/paratrack) | PUBLIC | 234 | 4 |  |
| [wiki-js](https://github.com/aa-blinov/wiki-js) | PRIVATE | 219 | 22 |  |
| [monos-home](https://github.com/aa-blinov/monos-home) | PRIVATE | 101 | 0 |  |
| [notes](https://github.com/aa-blinov/notes) | PRIVATE | 98 | 1 |  |
| [monos-sync-test](https://github.com/aa-blinov/monos-sync-test) | PRIVATE | 95 | 0 | Temporary private repo for verifying two-device sync. Safe to delete. |
| [petzy](https://github.com/aa-blinov/petzy) | PUBLIC | 95 | 3 |  |
| [stavki](https://github.com/aa-blinov/stavki) | PRIVATE | 73 | 3 | Доска для бытовых споров: лента, планка, счёт. Деньги не принимает |
| [cast](https://github.com/aa-blinov/cast) | PUBLIC | 70 | 2 | Minimal terminal coding agent with OpenAI-compatible routing. Works wi |
| [haven](https://github.com/aa-blinov/haven) | PUBLIC | 65 | 1 | Self-hosted private chat — No cloud, no telemetry, no Big Tech. Discor |
| [cast-team](https://github.com/aa-blinov/cast-team) | PRIVATE | 57 | 2 | Fork of cast exploring multi-user/team functionality |
| [monos](https://github.com/aa-blinov/monos) | PUBLIC | 57 | 2 | Local-first desktop notes app with Markdown, wiki links, full-text sea |
| [protokol](https://github.com/aa-blinov/protokol) | PRIVATE | 56 | 4 | Протокол — приватная расшифровка встреч. Аудио → транскрипт → маскиров |
| [flash-bar-delivery](https://github.com/aa-blinov/flash-bar-delivery) | PRIVATE | 48 | 1 | App for delivery (21+) |
| [doktor-ryadom](https://github.com/aa-blinov/doktor-ryadom) | PUBLIC | 45 | 0 | Рядом — дневник самочувствия пациента и кабинет врача |
| [the-cuba-times-tgif](https://github.com/aa-blinov/the-cuba-times-tgif) | PRIVATE | 43 | 1 | Simple landing for sunny Cuba |
| [qazaq-anki](https://github.com/aa-blinov/qazaq-anki) | PUBLIC | 41 | 2 | Spaced-repetition flashcards for learning Kazakh (CEFR A1–C1). SM-2 al |
| [lazy-to-text](https://github.com/aa-blinov/lazy-to-text) | PUBLIC | 39 | 1 | Local Whisper speech-to-text for Windows: global hotkey, Qt UI, no clo |
| [my-blog](https://github.com/aa-blinov/my-blog) | PUBLIC | 38 | 105 |  |
| [anki-bot](https://github.com/aa-blinov/anki-bot) | PRIVATE | 36 | 3 |  |
| [my-notes](https://github.com/aa-blinov/my-notes) | PRIVATE | 35 | 2 |  |
| [titles-forecating](https://github.com/aa-blinov/titles-forecating) | PUBLIC | 35 | 1 | Forecasting titles |
| [gambling-pack](https://github.com/aa-blinov/gambling-pack) | PRIVATE | 32 | 2 |  |
| [cronator](https://github.com/aa-blinov/cronator) | PUBLIC | 31 | 1 |  |
| [impeccable-mcode](https://github.com/aa-blinov/impeccable-mcode) | PUBLIC | 31 | 1 | Impeccable design skill for MiniMax Code — fork of pbakaus/impeccable  |
| [metronome](https://github.com/aa-blinov/metronome) | PRIVATE | 31 | 2 |  |
| [blog](https://github.com/aa-blinov/blog) | PRIVATE | 30 | 3 |  |
| [demo-platform](https://github.com/aa-blinov/demo-platform) | PRIVATE | 30 | 1 |  |
| [petzy-ios](https://github.com/aa-blinov/petzy-ios) | PUBLIC | 29 | 3 | Petzy для iOS: нативный SwiftUI-клиент дневника здоровья питомца, тот  |
| [templates-mcp](https://github.com/aa-blinov/templates-mcp) | PUBLIC | 29 | 0 | Reference template for building production-grade MCP servers for Bitri |
| [MediaSquash](https://github.com/aa-blinov/MediaSquash) | PRIVATE | 28 | 2 |  |
| [koloda](https://github.com/aa-blinov/koloda) | PUBLIC | 28 | 3 | Единая лента из Telegram-каналов: свой ридер с поиском, фильтрами и RS |
| [umnaya-alisa](https://github.com/aa-blinov/umnaya-alisa) | PRIVATE | 28 | 1 | Приватный навык Алисы: чат с MiniMax |
| [anki-service](https://github.com/aa-blinov/anki-service) | PRIVATE | 27 | 7 |  |
| [gchat-sentry-notifier](https://github.com/aa-blinov/gchat-sentry-notifier) | PUBLIC | 27 | 2 |  |
| [puuush](https://github.com/aa-blinov/puuush) | PUBLIC | 27 | 2 | Скриншот области экрана, загрузка, ссылка в буфере обмена. Electron-кл |
| [wallpaper-generator](https://github.com/aa-blinov/wallpaper-generator) | PUBLIC | 27 | 3 | 120 abstract-wallpaper generators running live in the browser — vanill |
| [cbr-currency-bot](https://github.com/aa-blinov/cbr-currency-bot) | PUBLIC | 25 | 2 |  |
| [crm-exporter](https://github.com/aa-blinov/crm-exporter) | PRIVATE | 25 | 3 |  |
| [docs](https://github.com/aa-blinov/docs) | PRIVATE | 25 | 3 |  |
| [gunicorn-stats](https://github.com/aa-blinov/gunicorn-stats) | PRIVATE | 25 | 2 |  |
| [rag](https://github.com/aa-blinov/rag) | PRIVATE | 25 | 2 |  |
| [alert-bot](https://github.com/aa-blinov/alert-bot) | PRIVATE | 24 | 3 |  |
| [cloud-cost-dashboard](https://github.com/aa-blinov/cloud-cost-dashboard) | PRIVATE | 24 | 2 | Прогноз расходов и разбор по ресурсам: immers.cloud + Yandex Cloud, да |
| [coop-watcher](https://github.com/aa-blinov/coop-watcher) | PRIVATE | 24 | 1 |  |
| [govno](https://github.com/aa-blinov/govno) | PRIVATE | 24 | 1 |  |
| [llm-code-review](https://github.com/aa-blinov/llm-code-review) | PRIVATE | 24 | 2 |  |
| [whisper-bot](https://github.com/aa-blinov/whisper-bot) | PUBLIC | 24 | 3 |  |
| [aa-blinov](https://github.com/aa-blinov/aa-blinov) | PUBLIC | 22 | 2 | Config files for my GitHub profile. |
| [cli_calendar](https://github.com/aa-blinov/cli_calendar) | PRIVATE | 22 | 2 |  |
| [crypto-service](https://github.com/aa-blinov/crypto-service) | PRIVATE | 22 | 2 |  |
| [simple-scripts-collection](https://github.com/aa-blinov/simple-scripts-collection) | PUBLIC | 22 | 2 |  |
| [monos-sync-e2e-1781381662822](https://github.com/aa-blinov/monos-sync-e2e-1781381662822) | PRIVATE | 21 | 3 | Monos real sync/conflict e2e test repo |
| [monos-sync-e2e-1781381831101](https://github.com/aa-blinov/monos-sync-e2e-1781381831101) | PRIVATE | 21 | 3 | Monos real sync/conflict e2e test repo |
| [monos-sync-matrix-1781382370490](https://github.com/aa-blinov/monos-sync-matrix-1781382370490) | PRIVATE | 21 | 3 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382440442](https://github.com/aa-blinov/monos-sync-matrix-1781382440442) | PRIVATE | 21 | 3 | Monos real sync edge-case matrix |
| [monos-sync-matrix-1781382482939](https://github.com/aa-blinov/monos-sync-matrix-1781382482939) | PRIVATE | 21 | 3 | Monos real sync edge-case matrix |
| [all-about-all](https://github.com/aa-blinov/all-about-all) | PRIVATE | 20 | 2 |  |
| [bitrix-mcp](https://github.com/aa-blinov/bitrix-mcp) | PUBLIC | 20 | 2 |  |
| [photo-checker](https://github.com/aa-blinov/photo-checker) | PUBLIC | 20 | 2 |  |
| [self-hosted-search-agent](https://github.com/aa-blinov/self-hosted-search-agent) | PUBLIC | 20 | 1 |  |
| [simple-rag](https://github.com/aa-blinov/simple-rag) | PUBLIC | 20 | 1 |  |
| [stt-yandex](https://github.com/aa-blinov/stt-yandex) | PUBLIC | 20 | 2 |  |
| [bspb-universal-helper-poc](https://github.com/aa-blinov/bspb-universal-helper-poc) | PRIVATE | 19 | 15 |  |
| [claude-gateway](https://github.com/aa-blinov/claude-gateway) | PUBLIC | 19 | 2 | OpenAI-compatible HTTP gateway over Claude Code CLI with real streamin |
| [course](https://github.com/aa-blinov/course) | PRIVATE | 19 | 0 |  |
| [projects-exporter](https://github.com/aa-blinov/projects-exporter) | PRIVATE | 19 | 2 |  |
| [roma-stt](https://github.com/aa-blinov/roma-stt) | PRIVATE | 19 | 2 |  |
| [codex-gateway](https://github.com/aa-blinov/codex-gateway) | PUBLIC | 18 | 2 | OpenAI-compatible HTTP wrapper over codex exec |
| [eora](https://github.com/aa-blinov/eora) | PRIVATE | 18 | 1 |  |
| [monos-conflict-test](https://github.com/aa-blinov/monos-conflict-test) | PRIVATE | 18 | 1 | Test repo for conflict resolution UI |
| [monos-notes](https://github.com/aa-blinov/monos-notes) | PRIVATE | 18 | 1 | Заметки Monos: синхронизация между устройствами |
| [ovh-caddy](https://github.com/aa-blinov/ovh-caddy) | PRIVATE | 18 | 1 | Машинный Caddy на VPS: все проекты за одним прокси |
| [ponytail-minimax](https://github.com/aa-blinov/ponytail-minimax) | PUBLIC | 18 | 1 | Ponytail lazy-senior-dev mode as a MiniMax Code plugin: the same six s |
| [spin-game](https://github.com/aa-blinov/spin-game) | PRIVATE | 18 | 1 |  |
| [vibe-vpn](https://github.com/aa-blinov/vibe-vpn) | PUBLIC | 18 | 2 |  |
| [monos-conflict-lab](https://github.com/aa-blinov/monos-conflict-lab) | PRIVATE | 17 | 1 | Monos sync conflict test sandbox |
| [bitrix-flow](https://github.com/aa-blinov/bitrix-flow) | PUBLIC | 16 | 2 |  |
| [project-setup-tool](https://github.com/aa-blinov/project-setup-tool) | PUBLIC | 16 | 1 |  |
| [trentini-poc](https://github.com/aa-blinov/trentini-poc) | PRIVATE | 16 | 17 |  |
| [better-ssh](https://github.com/aa-blinov/better-ssh) | PUBLIC | 11 | 2 | A friendlier layer over OpenSSH: interactive picker, encrypted passwor |
| [golden-repo](https://github.com/aa-blinov/golden-repo) | PUBLIC | 1 | 0 | The canonical house standard for every repository: one file tree, one  |

## The rules behind the codes

See [house-style.md](house-style.md) for what each code means and why
it exists, and [migration.md](migration.md) for the procedure.
