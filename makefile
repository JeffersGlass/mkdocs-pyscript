env := ./env

setup: 
	npm install
	$(CONDA_EXE) env $(shell [ -d .$(env) ] && echo update || echo create) -p $(env) --file environment.yml
	
build-js:
	npm run build
	cp -r mkdocs_pyscript/css mkdocs_pyscript/dist

build:
	make build-js
	python -m build