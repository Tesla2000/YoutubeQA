setup: git_init git_add poetry precommit_install

precommit_install:
	pre-commit install

git_init:
	git init

git_add:
	git add .

poetry:
	poetry init
	poetry add pre-commit black dynamic-executor

.PHONY: setup
