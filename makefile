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
	export DATABASE_URL=postgres://localhost/navigator; \
	export DJANGO_SETTINGS_MODULE=navigator.settings.dev; \
	export SECRET_KEY=secret; \
	export STORAGE_TYPE=local; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export FEATURE_EXPORT_JOURNEY_ENABLED=false; \
	export DIRECTORY_CONSTANTS_URL_EXPORT_READINESS=http://exred.trade.great:8007; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://supplier.trade.great:8005; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://invest.trade.great:8012; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004; \
	export ACTIVITY_STREAM_ACCESS_KEY_ID=1234-id-key; \
	export ACTIVITY_STREAM_SECRET_ACCESS_KEY=1234-secret-key

DJANGO_WEBSERVER := \
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
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && pycodestyle && $(PYTEST) && $(CODECOV)
