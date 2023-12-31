env := ./env

setup: 
	npm install
	pipenv install -d
	playwright install
	
build-js:
	npm run build
	cp -r mkdocs_pyscript/css mkdocs_pyscript/dist

build-dist:
	rm -rf ./dist
	rm -rf ./build
	make build-js
	python -m build
	twine check dist/*

test:
	make build-js
	pytest ./tests $(ARGS)

test-dev:
	PWDEBUG=1 pytest ./tests $(ARGS)

deploy-test:
	echo "Deploying a test.pypi.org"
	twine upload -r testpypi dist/*

deploy-real:
	make build-dist
	@read -p "Are you sure? [y/N] " ans && ans=$${ans:-N} ; \
    if [ $${ans} = y ] || [ $${ans} = Y ]; then \
        printf $(_SUCCESS) "Uploading to PyPI" ; \
		twine upload -r pypi dist/*; \
    else \
        printf $(_DANGER) "ABORTING UPLOAD" ; \
		exit 1; \
    fi
	echo "Deploying to pypi.org"

_SUCCESS := "\033[32m[%s]\033[0m %s\n" # Green text for "printf"
_DANGER := "\033[31m[%s]\033[0m %s\n" # Red text for "printf"