
clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

export PORT := ${DEV_PORT}

DEBUG_SET_ENV_VARS:= \
	export PORT=8008; \
	export DEBUG=True; \
	export DATABASE_URL=postgres://localhost/navigator; \
	export SECRET_KEY=debug; \
	export STORAGE_TYPE=local; \
	export ALLOWED_HOSTS=localhost,soo.trade.great; \
	export SOO_HOST=http://soo.trade.great:8008/; \
	export HELP_HOST=http://contact.trade.great:8009/; \
	export SSO_HOST=http://sso.trade.great:8004/; \
	export PROFILE_HOST=https://profile.trade.great:8006/; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/selling-online-overseas; \
	export GREAT_EXPORT_HOME=http://exred.trade.great:8007; \
	export EXPORTING_NEW=http://exred.trade.great:8007/new; \
	export CUSTOM_PAGE=http://exred.trade.great:8007/custom; \
	export EXPORTING_OCCASIONAL=http://exred.trade.great:8007/occasional; \
	export EXPORTING_REGULAR=http://exred.trade.great:8007/regular; \
	export GUIDANCE_MARKET_RESEARCH=http://exred.trade.great:8007/market-research; \
	export GUIDANCE_CUSTOMER_INSIGHT=http://exred.trade.great:8007/customer-insight; \
	export GUIDANCE_FINANCE=http://exred.trade.great:8007/finance; \
	export GUIDANCE_BUSINESS_PLANNING=http://exred.trade.great:8007/business-planning; \
	export GUIDANCE_GETTING_PAID=http://exred.trade.great:8007/getting-paid; \
	export GUIDANCE_OPERATIONS_AND_COMPLIANCE=http://exred.trade.great:8007/operations-and-compliance; \
	export SERVICES_EXOPPS=http://opportunities.export.great.gov.uk; \
	export SERVICES_FAB=http://buyer.trade.great:8001; \
	export SERVICES_GET_FINANCE=http://exred.trade.great:8007/get-finance; \
	export SERVICES_SOO=http://soo.trade.great:8008; \
	export INFO_TERMS_AND_CONDITIONS=http://exred.trade.great:8007/terms-and-conditions; \
	export INFO_ABOUT=http://exred.trade.great:8007/about; \
	export INFO_PRIVACY_AND_COOKIES=http://exred.trade.great:8007/privacy-and-cookies; \
	export SSO_PROXY_SIGNATURE_SECRET=proxy_signature_debug; \
	export SSO_PROXY_API_CLIENT_BASE_URL=http://sso.trade.great:8004/; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://soo.trade.great:8008; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/selling-online-overseas/; \
	export SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export SSO_PROXY_SESSION_COOKIE=debug_sso_session_cookie

TEST_SET_ENV_VARS:= \
	export SECRET_KEY=test; \
	export RESTRICT_IPS=false; \
	export STORAGE_TYPE=local; \
	export DATABASE_URL=postgres://localhost/navigator; \
	export DEBUG=True; \
	export ALLOWED_HOSTS=*; \
	export ADMINS=('David Downes', 'david@downes.co.uk'); \
	export ALLOW_AUTHENTICATED=True; \
	export ALLOW_ADMIN=True

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
	createdb navigator
	pip3 install -r requirements.txt
	$(DEBUG_SET_ENV_VARS) && \
	python app/manage.py migrate
	$(DEBUG_SET_ENV_VARS) && \
	python app/manage.py build_index
	npm install && npm run build
	npm run webdriver_update
	$(DEBUG_SET_ENV_VARS) && \
	python app/manage.py collectstatic --noinput

rebuild_docker:
	docker-compose rm -f
	docker images -q navigator_* | xargs docker rmi -f
	make build_docker

rebuild_local:
	dropdb navigator
	make build_local && \
	make run_local

debug_webserver:
	make run_local

run_docker:
	docker-compose up --build dev

run_local:
	$(DEBUG_SET_ENV_VARS) && \
	python app/manage.py collectstatic --noinput && \
	python app/manage.py runserver 0.0.0.0:$$PORT


test_docker:
	docker-compose up --build test

test_local:
	pep8 . --exclude .venv,node_modules
	npm test
	$(TEST_SET_ENV_VARS) && python app/manage.py collectstatic --noinput
	$(TEST_SET_ENV_VARS) && coverage run --source='.' app/manage.py test
	$(TEST_SET_ENV_VARS) && cd app && python manage.py test --noinput && cd -
