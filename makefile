deploy:
	docker-compose pull
	docker-compose build build
	docker-compose run build /project/deploy.sh


build_docker:
	docker-compose rm -f && \
	docker-compose pull
	docker-compose build test
	docker-compose build dev

build_local:
	./scripts/local/bootstrap.sh


rebuild_docker:
	docker-compose rm -f
	docker images -q navigator_* | xargs docker rmi -f
	make build_docker

rebuild_local:
	dropdb navigator
	./scripts/local/bootstrap.sh && \
	./scripts/local/web-start.sh

run_docker:
	docker-compose up --build dev

run_local:
	./scripts/local/web-start.sh

docker_test:
	docker-compose up --build test

compile_requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

upgrade_requirements:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements_test.in

DEBUG_SET_ENV_VARS := \
	export PORT=8008; \
	export DATABASE_URL=postgres://debug:debug@localhost/navigator; \
	export SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://buyer.trade.great:8001; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/find-a-buyer/; \
	export SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export DJANGO_SETTINGS_MODULE=navigator.settings.dev; \
	export SECRET_KEY=secret; \
	export STORAGE_TYPE=local; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export FEATURE_EXPORT_JOURNEY_ENABLED=false; \
	export DIRECTORY_SSO_API_CLIENT_BASE_URL=http://sso.trade.great:8003/; \
	export DIRECTORY_SSO_API_CLIENT_API_KEY=api_signature_debug; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/?next=http://soo.trade.great:8008; \
	export SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://soo.trade.great:8008; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/?next=http://soo.trade.great:8008; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/selling-online-overseas/; \
	export SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://supplier.trade.great:8005; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://invest.trade.great:8012; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004; \
	export ACTIVITY_STREAM_ACCESS_KEY_ID=1234-id-key; \
	export ACTIVITY_STREAM_SECRET_ACCESS_KEY=1234-secret-key; \
	export FEATURE_NEW_HEADER_FOOTER_ENABLED=true; \
	export FEATURE_HEADER_SEARCH_ENABLED=false; \
	export STATIC_HOST=http://0.0.0.0:$$PORT/selling-online-overseas

DJANGO_WEBSERVER := \
	python app/manage.py migrate && \
	python app/manage.py build_index && \
	python ./app/manage.py collectstatic --noinput && \
	python ./app/manage.py runserver 0.0.0.0:$$PORT --settings=navigator.settings.dev

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && python ./app/manage.py shell

debug_manage:
	$(DEBUG_SET_ENV_VARS) && python ./app/manage.py $(cmd)

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 app --exclude=migrations,.venv
PYTEST := pytest ./app -v --ignore=node_modules --cov=./app --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python ./app/manage.py collectstatic --noinput
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(COLLECT_STATIC) && pycodestyle && $(PYTEST) && $(CODECOV)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && pycodestyle --exclude=.venv,node_modules && $(PYTEST) && $(CODECOV)
