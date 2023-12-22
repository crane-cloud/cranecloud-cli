build: venv # build the project
	@ ${INFO} "Building required distribution"
	@ source venv/bin/activate && python3 -m build
	@ ${INFO} "Distribution successfully built"
	@ echo " "


install: venv # install the package
	@ ${INFO} "Installing the package"
	@ source venv/bin/activate && pip3 install -e .
	@ ${INFO} "Project successfully installed"
	@ echo " "

compile-req: venv # compile the requirements
	@ ${INFO} "Compiling requirements"
	@ source venv/bin/activate && pip-compile pyproject.toml --extra dev pyproject.toml
	@ ${INFO} "Requirements successfully compiled"
	@ echo " "

sync-req: venv # sync the requirements
	@ ${INFO} "Syncing requirements"
	@ source venv/bin/activate && pip-sync requirements.txt
	@ ${INFO} "Requirements successfully synced"
	@ echo " "

upload: venv # upload the package to pypi
	@ ${INFO} "Uploading the package to pypi"
	@ source venv/bin/activate && python3 -m twine upload -r testpypi dist/*
	@ ${INFO} "Package successfully uploaded"
	@ echo " "

# set default target
.DEFAULT_GOAL := help

# colors
YELLOW := $(shell tput -Txterm setaf 3)
NC := "\e[0m"

#shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE