include build.env

setenv PORT=${DEV_PORT}

build: build_${NAV_BUILD_TYPE}

run: run_${NAV_BUILD_TYPE}

test: test_${NAV_BUILD_TYPE}

rebuild: rebuild_${NAV_BUILD_TYPE}

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


test_docker:
	docker-compose up --build test

test_local:
	./scripts/local/run_tests.sh
