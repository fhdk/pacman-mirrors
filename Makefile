.PHONY: clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "tests - run all tests"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "build-doc - generate MkDocs HTML documentation, man page using Pandoc, including API docs"
	@echo "install-dev - install in venv"
	@echo "run-dev - run in venv"
	@echo "extract-pot - extract messages to locale/messages.pot"
	@echo "compile-mo -compile pot messages to locale/"
	@echo "push-pot - push pot file to transifex"
	@echo "pull-po - pull all translations from transifex"

clean: clean-build clean-test
tests: lint unit-test
build: extract-pot compile-mo
    poetry build

clean-build:
	rm -fr dist/

clean-test:
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 pacman_mirrors tests

unit-test:
	poetry run pytest

coverage:
	coverage run pacman_mirrors tests 
	coverage report -m
	coverage html
	firefox htmlcov/index.html

build-doc:
	mkdocs build
	pandoc -s -t man docs/index.md -o build/man/pacman-mirrors.8
	pandoc docs/index.md -f markdown -t html -s -o build/man/pacman-mirrors.8.html
	gzip build/man/pacman-mirrors.8 -fq

install-dev: clean mo-files
	poetry install

run-dev:
    poetry run pacman_mirrors

extract-pot:
	pybabel extract --input-dirs=pacman_mirrors --output-file=locale/pacman_mirrors.pot

compile-mo:
	pybabel compile -D pacman_mirrors -d locale

push-pot:
	tx push -s

pull-po:
	tx pull -a
