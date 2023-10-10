env := ./env

setup: 
	npm install
	$(CONDA_EXE) env $(shell [ -d .$(env) ] && echo update || echo create) -p $(env) --file environment.yml
	
build:
	npm run build