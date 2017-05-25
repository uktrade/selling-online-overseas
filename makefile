include build.env


build: build_${NAV_BUILD_TYPE}

run: run_${NAV_BUILD_TYPE}

test: test_${NAV_BUILD_TYPE}

rebuild: rebuild_${NAV_BUILD_TYPE}


build_docker: 
	docker-compose rm -f && \
	docker-compose pull
	docker-compose build test
	docker-compose build web

build_local:
	./scripts/local/bootstrap.sh


rebuild_docker:
	docker-compose rm -f
	docker rmi -f $(docker images -q navigator_*)
	build_docker

rebuild_local:
	dropdb navigator
	./scripts/local/bootstrap.sh && \
	./scripts/local/web-start.sh


run_docker: 
	docker-compose up web

run_local:
	./scripts/local/web-start.sh


test_docker:
	docker-compose up --build test

test_local:
	./scripts/local/run_tests.sh
