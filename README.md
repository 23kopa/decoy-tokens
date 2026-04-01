
```
decoy-tokens
├─ Makefile
├─ README copy.md
├─ README.md
├─ alembic.ini
├─ backend
│  ├─ Dockerfile
│  ├─ Dockerfile.prod
│  ├─ alembic
│  │  ├─ README
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     ├─ 3964fb20af0c_drop_token_secret_hash.py
│  │     ├─ f18364e61213_initial_migration.py
│  │     └─ f5347ef63ae6_add_token_slug_and_backfill.py
│  └─ app
│     ├─ __init__.py
│     ├─ application
│     │  ├─ __init__.py
│     │  ├─ errors.py
│     │  ├─ ports
│     │  │  ├─ __init__.py
│     │  │  ├─ dedup_store.py
│     │  │  ├─ event_repository.py
│     │  │  ├─ rate_limiter.py
│     │  │  ├─ token_repository.py
│     │  │  └─ user_repository.py
│     │  └─ use_cases
│     │     ├─ __init__.py
│     │     ├─ events
│     │     │  ├─ get_token_events.py
│     │     │  ├─ get_tokens_stats.py
│     │     │  └─ log_token_event.py
│     │     ├─ tokens
│     │     │  ├─ activate_token.py
│     │     │  ├─ create_token.py
│     │     │  ├─ list_user_tokens.py
│     │     │  └─ set_token_active.py
│     │     └─ user
│     │        ├─ authenticate.py
│     │        └─ register.py
│     ├─ core
│     │  ├─ __init__.py
│     │  └─ config.py
│     ├─ data
│     │  ├─ geoip
│     │  │  ├─ GeoLite2-ASN.mmdb
│     │  │  ├─ GeoLite2-City.mmdb
│     │  │  └─ geoip.zip
│     │  └─ media
│     │     ├─ favicons
│     │     │  └─ tokenguard.svg
│     │     └─ gifs
│     │        └─ spbgut.gif
│     ├─ domain
│     │  ├─ __init__.py
│     │  ├─ entities
│     │  │  ├─ token.py
│     │  │  ├─ token_event.py
│     │  │  └─ user.py
│     │  ├─ policies
│     │  └─ value
│     │     └─ email.py
│     ├─ infrastructure
│     │  ├─ __init__.py
│     │  ├─ database
│     │  │  ├─ __init__.py
│     │  │  ├─ base.py
│     │  │  ├─ engine.py
│     │  │  ├─ mappers
│     │  │  │  ├─ token.py
│     │  │  │  ├─ token_event.py
│     │  │  │  └─ user.py
│     │  │  ├─ models
│     │  │  │  ├─ __init__.py
│     │  │  │  ├─ token.py
│     │  │  │  ├─ token_event.py
│     │  │  │  └─ user.py
│     │  │  └─ repositories
│     │  │     ├─ __init__.py
│     │  │     ├─ token.py
│     │  │     ├─ token_event
│     │  │     │  ├─ __init__.py
│     │  │     │  ├─ crud.py
│     │  │     │  ├─ stats.py
│     │  │     │  └─ update.py
│     │  │     └─ user.py
│     │  ├─ http
│     │  │  └─ token_request_collector.py
│     │  ├─ security
│     │  │  ├─ password.py
│     │  │  └─ recaptcha.py
│     │  └─ utils
│     │     ├─ logging.py
│     │     └─ slug.py
│     ├─ main.py
│     ├─ services
│     │  ├─ __init__.py
│     │  └─ decoy_tokens
│     │     ├─ __init__.py
│     │     ├─ engines
│     │     │  ├─ __init__.py
│     │     │  ├─ email.py
│     │     │  └─ link.py
│     │     └─ utils
│     │        ├─ __init__.py
│     │        ├─ detectors
│     │        │  ├─ __init__.py
│     │        │  ├─ bot.py
│     │        │  └─ dedup.py
│     │        ├─ fingerprint
│     │        │  ├─ __init__.py
│     │        │  └─ generate.py
│     │        ├─ geo
│     │        │  └─ geoip.py
│     │        ├─ headers
│     │        │  ├─ __init__.py
│     │        │  ├─ extractor.py
│     │        │  ├─ parser copy.py
│     │        │  └─ parser.py
│     │        └─ ip
│     │           ├─ __init__.py
│     │           ├─ detection.py
│     │           ├─ detection_trusted.py
│     │           ├─ proxy.py
│     │           └─ validation.py
│     ├─ static
│     │  ├─ .vite
│     │  │  └─ manifest.json
│     │  ├─ css
│     │  │  └─ style.css
│     │  └─ js
│     │     └─ main.js
│     ├─ templates
│     │  ├─ components
│     │  │  ├─ dashboard
│     │  │  │  ├─ events
│     │  │  │  │  ├─ general
│     │  │  │  │  │  ├─ all_headers_card.html
│     │  │  │  │  │  ├─ behavior_card.html
│     │  │  │  │  │  ├─ client_card.html
│     │  │  │  │  │  ├─ ip_history_card.html
│     │  │  │  │  │  ├─ network_card.html
│     │  │  │  │  │  └─ timeline_card.html
│     │  │  │  │  └─ navigation
│     │  │  │  │     └─ event_card.html
│     │  │  │  └─ page
│     │  │  │     ├─ activity_chart.html
│     │  │  │     ├─ tokens_list.html
│     │  │  │     └─ user_stats.html
│     │  │  ├─ home
│     │  │  │  ├─ page
│     │  │  │  │  ├─ help_steps.html
│     │  │  │  │  ├─ tips_secton.html
│     │  │  │  │  └─ tokens_store.html
│     │  │  │  └─ token
│     │  │  │     └─ create_token_form.html
│     │  │  └─ shared
│     │  │     ├─ gif_viewer.html
│     │  │     └─ notifications.html
│     │  ├─ layouts
│     │  │  ├─ base.html
│     │  │  ├─ private.html
│     │  │  └─ public.html
│     │  ├─ macros
│     │  │  ├─ cards
│     │  │  │  ├─ event_card.html
│     │  │  │  ├─ token_item.html
│     │  │  │  └─ token_preview.html
│     │  │  ├─ icons
│     │  │  │  ├─ base.html
│     │  │  │  ├─ chevron.html
│     │  │  │  └─ types.html
│     │  │  └─ ui
│     │  │     ├─ _ui.html
│     │  │     ├─ badges.html
│     │  │     ├─ buttons.html
│     │  │     ├─ fields.html
│     │  │     ├─ forms.html
│     │  │     └─ modal.html
│     │  ├─ modals
│     │  │  ├─ auth
│     │  │  │  ├─ login.html
│     │  │  │  └─ register.html
│     │  │  ├─ events
│     │  │  │  └─ token_event.html
│     │  │  ├─ shared
│     │  │  │  └─ confirm.html
│     │  │  └─ token
│     │  │     └─ create_token.html
│     │  ├─ pages
│     │  │  ├─ dashboard.html
│     │  │  ├─ hello.html
│     │  │  └─ home.html
│     │  └─ partials
│     │     ├─ headers
│     │     │  ├─ dashboard_header.html
│     │     │  ├─ hello_header.html
│     │     │  └─ home_header.html
│     │     ├─ modals
│     │     │  ├─ events
│     │     │  │  ├─ details.html
│     │     │  │  ├─ empty.html
│     │     │  │  ├─ events.html
│     │     │  │  ├─ footer.html
│     │     │  │  └─ header.html
│     │     │  └─ tokens
│     │     │     ├─ create_state.html
│     │     │     ├─ progress_state.html
│     │     │     └─ result_state.html
│     │     └─ navigation
│     │        └─ navbar.html
│     └─ web
│        ├─ dependencies
│        │  ├─ __init__.py
│        │  ├─ current_user.py
│        │  ├─ db.py
│        │  └─ use_cases.py
│        ├─ middlewares
│        │  ├─ __init__.py
│        │  ├─ csrf.py
│        │  ├─ rate_limit.py
│        │  ├─ sessions.py
│        │  └─ test_headers.py
│        ├─ presenters
│        │  └─ events
│        │     ├─ behavior_presenter.py
│        │     ├─ client_presenter.py
│        │     ├─ headers_presenter.py
│        │     ├─ history_presenter.py
│        │     ├─ network_presenter.py
│        │     └─ timeline_presenter.py
│        ├─ routes
│        │  ├─ __init__.py
│        │  ├─ api
│        │  │  └─ v1
│        │  │     ├─ __init__.py
│        │  │     ├─ dependencies.py
│        │  │     ├─ events
│        │  │     │  ├─ presenter.py
│        │  │     │  ├─ routes.py
│        │  │     │  └─ schemas.py
│        │  │     └─ tokens
│        │  │        ├─ routes.py
│        │  │        └─ schemas.py
│        │  ├─ pages
│        │  │  ├─ __init__.py
│        │  │  ├─ private
│        │  │  │  ├─ dashboard.py
│        │  │  │  └─ home.py
│        │  │  └─ public
│        │  │     ├─ auth.py
│        │  │     └─ landing.py
│        │  └─ public
│        │     └─ tokens
│        │        └─ trigger.py
│        └─ security
│           ├─ jwt_token.py
│           └─ permissions.py
├─ deploy
│  └─ nginx
│     └─ default.conf
├─ docker-compose.prod.yml
├─ docker-compose.yml
├─ frontend
│  ├─ .vite
│  │  └─ deps
│  │     ├─ _metadata.json
│  │     └─ package.json
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ src
│  │  ├─ input.css
│  │  ├─ main.js
│  │  ├─ modules
│  │  │  ├─ events
│  │  │  │  ├─ components
│  │  │  │  │  └─ tokenEvents.js
│  │  │  │  ├─ index.js
│  │  │  │  ├─ services
│  │  │  │  │  └─ eventTokenService.js
│  │  │  │  ├─ stores
│  │  │  │  │  ├─ tokenEventsModalStore.js
│  │  │  │  │  └─ tokenEventsStoreBridge.js
│  │  │  │  └─ utils
│  │  │  │     └─ eventPresentation.js
│  │  │  ├─ index.js
│  │  │  ├─ shared
│  │  │  │  └─ utils
│  │  │  │     ├─ api.js
│  │  │  │     ├─ buttonFeedback.js
│  │  │  │     ├─ clipboard.js
│  │  │  │     ├─ directives
│  │  │  │     │  └─ loadingButton.js
│  │  │  │     ├─ logger.js
│  │  │  │     └─ notification.js
│  │  │  └─ tokens
│  │  │     ├─ components
│  │  │     │  └─ tokenCreate.js
│  │  │     ├─ index.js
│  │  │     ├─ services
│  │  │     │  └─ createTokenService.js
│  │  │     └─ utils
│  │  │        └─ tokenProgressAnimation.js
│  │  └─ styles
│  │     ├─ base
│  │     │  └─ variables.css
│  │     ├─ components
│  │     │  ├─ cards.css
│  │     │  ├─ components.css
│  │     │  ├─ modals.css
│  │     │  ├─ pages.css
│  │     │  └─ sections.css
│  │     ├─ main.css
│  │     ├─ themes
│  │     └─ utilities
│  │        └─ scrollbar.css
│  └─ vite.config.js
├─ requirements.txt
├─ scripts
│  ├─ auto-backup.sh
│  ├─ backup.sh
│  ├─ prepare-front.sh
│  ├─ prod-deploy.sh
│  └─ status-check.sh
└─ uv.lock

```