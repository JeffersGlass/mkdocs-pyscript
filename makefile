env := ./env

setup: 
	$(CONDA_EXE) env $(shell [ -d .$(env) ] && echo update || echo create) -p $(env) --file environment.yml