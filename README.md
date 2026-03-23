
```
decoy-tokens
├─ Makefile
├─ README.dev.md
├─ README.md
├─ backend
│  ├─ Dockerfile
│  ├─ Dockerfile.prod
│  ├─ alembic
│  │  ├─ README
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     └─ f18364e61213_initial_migration.py
│  ├─ app
│  │  ├─ __init__.py
│  │  ├─ application
│  │  │  ├─ __init__.py
│  │  │  ├─ domain
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ entities
│  │  │  │  │  └─ user.py
│  │  │  │  └─ value_objects
│  │  │  │     └─ email.py
│  │  │  ├─ ports
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ user_repository.py
│  │  │  └─ use_cases
│  │  │     ├─ __init__.py
│  │  │     └─ user
│  │  │        ├─ authenticate.py
│  │  │        └─ register.py
│  │  ├─ core
│  │  │  ├─ __init__.py
│  │  │  ├─ config.py
│  │  │  ├─ logging.py
│  │  │  └─ security.py
│  │  ├─ infrastructure
│  │  │  ├─ __init__.py
│  │  │  └─ database
│  │  │     ├─ __init__.py
│  │  │     ├─ base.py
│  │  │     ├─ engine.py
│  │  │     ├─ mappers
│  │  │     │  └─ user.py
│  │  │     ├─ models
│  │  │     │  ├─ __init__.py
│  │  │     │  ├─ token.py
│  │  │     │  ├─ token_event.py
│  │  │     │  └─ user.py
│  │  │     └─ repositories
│  │  │        ├─ __init__.py
│  │  │        ├─ token.py
│  │  │        ├─ token_event
│  │  │        │  ├─ __init__.py
│  │  │        │  ├─ crud.py
│  │  │        │  ├─ stats.py
│  │  │        │  └─ update.py
│  │  │        └─ user.py
│  │  ├─ main.py
│  │  ├─ services
│  │  │  ├─ __init__.py
│  │  │  └─ decoy_tokens
│  │  │     ├─ __init__.py
│  │  │     ├─ collector.py
│  │  │     ├─ engines
│  │  │     │  ├─ __init__.py
│  │  │     │  ├─ email.py
│  │  │     │  └─ link.py
│  │  │     ├─ events.py
│  │  │     ├─ security.py
│  │  │     ├─ shared
│  │  │     │  └─ logging.py
│  │  │     └─ utils
│  │  │        ├─ __init__.py
│  │  │        ├─ detectors
│  │  │        │  ├─ __init__.py
│  │  │        │  ├─ bot.py
│  │  │        │  └─ dedup.py
│  │  │        ├─ fingerprint
│  │  │        │  ├─ __init__.py
│  │  │        │  └─ generate.py
│  │  │        ├─ geo
│  │  │        │  └─ geoip.py
│  │  │        ├─ headers
│  │  │        │  ├─ __init__.py
│  │  │        │  └─ extractor.py
│  │  │        └─ ip
│  │  │           ├─ __init__.py
│  │  │           ├─ detection.py
│  │  │           ├─ detection_trusted.py
│  │  │           ├─ proxy.py
│  │  │           └─ validation.py
│  │  ├─ static
│  │  │  ├─ .vite
│  │  │  │  └─ manifest.json
│  │  │  ├─ css
│  │  │  │  └─ style.css
│  │  │  └─ js
│  │  │     ├─ main.js
│  │  │     └─ main.js.map
│  │  ├─ templates
│  │  │  ├─ components
│  │  │  │  ├─ dashboard
│  │  │  │  │  ├─ events
│  │  │  │  │  │  ├─ general
│  │  │  │  │  │  │  ├─ fingerprint_card.html
│  │  │  │  │  │  │  ├─ ip_card.html
│  │  │  │  │  │  │  ├─ location_card.html
│  │  │  │  │  │  │  ├─ provider_card.html
│  │  │  │  │  │  │  └─ timeline_card.html
│  │  │  │  │  │  ├─ headers
│  │  │  │  │  │  │  ├─ accept_card.html
│  │  │  │  │  │  │  ├─ accept_encoding_card.html
│  │  │  │  │  │  │  ├─ accept_language_card.html
│  │  │  │  │  │  │  ├─ all_headers_card.html
│  │  │  │  │  │  │  ├─ connection_card.html
│  │  │  │  │  │  │  └─ user_agent_card.html
│  │  │  │  │  │  ├─ history
│  │  │  │  │  │  │  └─ ip_history_card.html
│  │  │  │  │  │  └─ navigation
│  │  │  │  │  │     └─ event_card.html
│  │  │  │  │  └─ page
│  │  │  │  │     ├─ activity_chart.html
│  │  │  │  │     ├─ tokens_list.html
│  │  │  │  │     └─ user_stats.html
│  │  │  │  ├─ home
│  │  │  │  │  ├─ page
│  │  │  │  │  │  ├─ help_steps.html
│  │  │  │  │  │  ├─ tips_secton.html
│  │  │  │  │  │  └─ tokens_store.html
│  │  │  │  │  └─ token
│  │  │  │  │     └─ create_token_form.html
│  │  │  │  └─ shared
│  │  │  │     ├─ gif_viewer.html
│  │  │  │     └─ notifications.html
│  │  │  ├─ layouts
│  │  │  │  ├─ base.html
│  │  │  │  ├─ private.html
│  │  │  │  └─ public.html
│  │  │  ├─ macros
│  │  │  │  ├─ cards
│  │  │  │  │  ├─ token_item.html
│  │  │  │  │  └─ token_preview.html
│  │  │  │  ├─ icons
│  │  │  │  │  ├─ base.html
│  │  │  │  │  ├─ chevron.html
│  │  │  │  │  └─ types.html
│  │  │  │  └─ ui
│  │  │  │     ├─ _ui.html
│  │  │  │     ├─ badges.html
│  │  │  │     ├─ buttons.html
│  │  │  │     ├─ fields.html
│  │  │  │     ├─ forms.html
│  │  │  │     └─ modal.html
│  │  │  ├─ modals
│  │  │  │  ├─ auth
│  │  │  │  │  ├─ login.html
│  │  │  │  │  └─ register.html
│  │  │  │  ├─ events
│  │  │  │  │  └─ token_event.html
│  │  │  │  ├─ shared
│  │  │  │  │  └─ confirm.html
│  │  │  │  └─ token
│  │  │  │     └─ create_token.html
│  │  │  ├─ pages
│  │  │  │  ├─ dashboard.html
│  │  │  │  ├─ hello.html
│  │  │  │  └─ home.html
│  │  │  └─ partials
│  │  │     ├─ headers
│  │  │     │  ├─ dashboard_header.html
│  │  │     │  ├─ hello_header.html
│  │  │     │  ├─ hello_header_v2.html
│  │  │     │  └─ home_header.html
│  │  │     ├─ modals
│  │  │     │  ├─ events
│  │  │     │  │  ├─ details.html
│  │  │     │  │  ├─ empty.html
│  │  │     │  │  ├─ events.html
│  │  │     │  │  ├─ footer.html
│  │  │     │  │  └─ header.html
│  │  │     │  └─ tokens
│  │  │     │     ├─ create_state.html
│  │  │     │     ├─ progress_state.html
│  │  │     │     └─ result_state.html
│  │  │     └─ navigation
│  │  │        └─ navbar.html
│  │  └─ web
│  │     ├─ __init__.py
│  │     ├─ api
│  │     │  └─ v1
│  │     │     ├─ __init__.py
│  │     │     ├─ auth
│  │     │     │  ├─ routes.py
│  │     │     │  └─ schemas.py
│  │     │     ├─ dependencies.py
│  │     │     ├─ events
│  │     │     │  ├─ routes.py
│  │     │     │  └─ schemas.py
│  │     │     └─ tokens
│  │     │        ├─ routes.py
│  │     │        └─ schemas.py
│  │     ├─ core
│  │     │  ├─ dependencies
│  │     │  │  ├─ __init__.py
│  │     │  │  ├─ current_user.py
│  │     │  │  ├─ db.py
│  │     │  │  └─ use_cases.py
│  │     │  └─ middlewares
│  │     │     ├─ __init__.py
│  │     │     ├─ sessions.py
│  │     │     └─ test_headers.py
│  │     ├─ pages
│  │     │  ├─ __init__.py
│  │     │  ├─ private
│  │     │  │  ├─ dashboard.py
│  │     │  │  └─ home.py
│  │     │  └─ public
│  │     │     ├─ auth.py
│  │     │     └─ landing.py
│  │     └─ public
│  │        └─ tokens
│  │           └─ trigger.py
│  └─ tests
│     ├─ conftest.py
│     ├─ e2e
│     │  └─ test_token_flow.py
│     ├─ fixtures
│     │  ├─ geo_data.py
│     │  ├─ headers.py
│     │  ├─ ip
│     │  │  └─ ip_data.py
│     │  └─ requests.py
│     └─ unit
│        └─ services
│           └─ decoy_tokens
│              └─ utils
│                 ├─ geo
│                 │  └─ test_geoip.py
│                 └─ ip
│                    ├─ test_detection.py
│                    ├─ test_proxy.py
│                    └─ test_validation.py
├─ constraints.txt
├─ deploy
│  └─ nginx
│     ├─ default.conf
│     └─ default.conf.https
├─ docker-compose.prod.yml
├─ docker-compose.yml
├─ frontend
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
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
├─ pytest.ini
├─ scripts
│  ├─ entrypoint.sh
│  ├─ migrate.sh
│  ├─ restart_db_dev.sh
│  └─ wait_for_postgres.sh
└─ uv.lock

```