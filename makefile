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

upgrade_requirements:
	pip-compile --upgrade requirements.in

compile_test_requirements:
	pip-compile requirements_test.in

upgrade_test_requirements:
	pip-compile --upgrade requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

upgrade_all_requirements: upgrade_requirements upgrade_test_requirements

test_requirements:
	pip install -r requirements_test.txt
