env := ./env

setup: 
	npm install
	conda env $(shell [ -d .$(env) ] && echo update || echo create) -p $(env) --file environment.yml
	
build-js:
	npm run build
	cp -r mkdocs_pyscript/css mkdocs_pyscript/dist

build:
	rm -r ./dist
	make build-js
	python -m build
	twine check dist/*

deploy-test:
	echo "Deploying a test to test.pypi.org"
	twine upload -r testpypi dist/*

deploy-real:
	@read -p "Are you sure? [y/N] " ans && ans=$${ans:-N} ; \
    if [ $${ans} = y ] || [ $${ans} = Y ]; then \
        printf $(_SUCCESS) "Uploading to PyPI" ; \
		twine upload -r pypi dist/*; \
    else \
        printf $(_DANGER) "ABORTING UPLOAD" ; \
		exit 1; \
    fi
	echo "Deployingto pypi.org"

_SUCCESS := "\033[32m[%s]\033[0m %s\n" # Green text for "printf"
_DANGER := "\033[31m[%s]\033[0m %s\n" # Red text for "printf"