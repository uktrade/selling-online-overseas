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

debug_webserver:
	make run_local

run_docker:
	docker-compose up --build dev

run_local:
	./scripts/local/web-start.sh

test_docker:
	docker-compose up --build test

compile_requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

upgrade_requirements:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements_test.in

DEBUG_SET_ENV_VARS := \
	export DATABASE_URL=postgres://localhost/navigator; \
	export DJANGO_SETTINGS_MODULE=navigator.settings.dev; \
	export SECRET_KEY=secret; \
	export STORAGE_TYPE=local

debug_shell:
	$(DEBUG_SET_ENV_VARS) && python ./app/manage.py shell

test_requirements:
	pip install -r requirements_test.txt

PYTEST := pytest ./app -v --ignore=node_modules --cov=./app --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python ./app/manage.py collectstatic --noinput
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(COLLECT_STATIC) && pep8 app && $(PYTEST) && $(CODECOV)
