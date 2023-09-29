.PHONY: clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "tests - run all tests"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "build-doc - generate MkDocs HTML documentation, man page usin ePandoc, includin eAPI docs"
	@echo "install-dev - install in venv"
	@echo "run-dev - run in venv"
	@echo "extract-pot - extract messages to locale/messages.pot"
	@echo "compile-mo -compile pot messages to locale/"
	@echo "push-pot - push pot file to transifex"
	@echo "pull-po - pull all translations from transifex"

clean: clean-build clean-test
tests: lint unit-test
build: extract-pot compile-mo build-man
	poetry build

clean-build:
	rm -fr dist/
	rm -fr build/

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

build-doc: clean-build
	mkdocs build

build-man:
	pandoc data/docs/index.md -f markdown -t html -s -o data/man/pacman-mirrors.8.html
	pandoc -s -t man data/docs/index.md -o data/man/pacman-mirrors.8
	gzip data/man/pacman-mirrors.8 -fq

extract-pot:
	pybabel extract --input-dirs=pacman_mirrors --output-file=data/locale/pacman_mirrors.pot

compile-mo:
	pybabel compile -D pacman_mirrors -d data/locale

push-pot:
	tx push -s

pull-po:
	tx pull -a

install-dev: install-data
	poetry install

run-dev:
	poetry run pacman_mirrors

install: build install-data

install-data:
	install -D data/share/mirrors.json /usr/share/pacman-mirrors/mirrors.json
	install -D data/etc/pacman-mirrors.conf /etc/
	install -D data/bin/pacman-mirrors /usr/bin/
	install -D data/man/pacman-mirrors.8.gz /usr/share/man/man8/
	install -D data/locale/es/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/es/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/de/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/de/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/eo/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/eo/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/zh_CN/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/zh_CN/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/hr/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/hr/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/tr/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/tr/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/be/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/be/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/cy/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/cy/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ko/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ko/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sw/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sw/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sk/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sk/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/fi/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/fi/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/es_AR/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/es_AR/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ru_RU/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ru_RU/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sk_SK/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sk_SK/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sr/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sr/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/fr/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/fr/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ar/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ar/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/hi/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/hi/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ro/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ro/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/is/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/is/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/uk/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/uk/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/tr_TR/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ca/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ca/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/mk/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/mk/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sq/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sq/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/gl_ES/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/gl_ES/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ca@valencia/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ca@valencia/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/zh_TW/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/zh_TW/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/pt_PT/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/pt_PT/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/hr_HR/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/hr_HR/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/hu/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/hu/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/el/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/el/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/bg/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/bg/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/pl/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/pl/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/kk/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/kk/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/az_AZ/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/az_AZ/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/lt/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/lt/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/is_IS/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/is_IS/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/pt/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/pt/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/da/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/da/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/nl/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/nl/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/es_ES/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/es_ES/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/id_ID/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/id_ID/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/cs/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/cs/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/es_419/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/es_419/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/he/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/he/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/sv/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/sv/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/et/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/et/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/pt_BR/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/pt_BR/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/it/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/it/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/uk_UA/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/uk_UA/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/hi_IN/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/hi_IN/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ja/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ja/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/fa/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/fa/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/or/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/or/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/ko_KR/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/ko_KR/LC_MESSAGES/pacman_mirrors.mo
	install -D data/locale/nb/LC_MESSAGES/pacman_mirrors.po /usr/share/locale/nb/LC_MESSAGES/pacman_mirrors.mo

uninstall:
	rm /usr/share/pacman-mirrors/mirrors.json
	rm /etc/pacman-mirrors.conf
	rm /usr/bin/pacman-mirrors
	rm /usr/share/man/man8/pacman-mirrors.8.gz
	rm /usr/share/locale/es/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/de/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/eo/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/zh_CN/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/hr/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/tr/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/be/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/cy/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ko/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sw/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sk/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/fi/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/es_AR/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ru_RU/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sk_SK/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sr/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/fr/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ar/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/hi/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ro/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/is/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/uk/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ca/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/mk/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sq/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/gl_ES/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ca@valencia/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/zh_TW/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/pt_PT/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/hr_HR/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/hu/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/el/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/bg/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/pl/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/kk/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/az_AZ/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/lt/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/is_IS/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/pt/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/da/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/nl/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/es_ES/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/id_ID/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/cs/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/es_419/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/he/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/sv/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/et/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/pt_BR/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/it/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/uk_UA/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/hi_IN/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ja/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/fa/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/or/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/ko_KR/LC_MESSAGES/pacman_mirrors.mo
	rm /usr/share/locale/nb/LC_MESSAGES/pacman_mirrors.mo
