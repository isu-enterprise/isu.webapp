.PHONY: env dev develop install test edit \
	py pot init-ru update-ru comp-cat \
	upd-cat setup test setup-requs tests \
	run-tests gdb-test clean serve server serv \
	template admin

LCAT=src/isu/webapp/locales

server: serve
serv: serve

template:
	(cd src/isu/webapp; ./install-admin-lte.sh)

admin: template

serve:
	pserve development.ini --reload

env:
	easy_install --upgrade pip

pre-dev:env #dev-....
	easy_install pip setuptools

setup:
	python setup.py build_ext # -L$(LG_LIB_DIR) -R$(LG_LIB_DIR) -I$(LG_HEADERS)
	python setup.py develop

dev:	pre-dev setup-requs setup # upd-cat

develop: dev

install: env comp-cat
	python setup.py install

edit:
	cd src && emacs

setup-requs: requirements.txt
	pip install -r requirements.txt

run-tests:
	nosetests -w src/tests

tests:	run-tests

test:	setup run-tests

gdb-test: setup
	gdb --args python nosetests -w src/tests

py:
	python

pot:
	mkdir -p $(LCAT)
	# rm $(LCAT)/messages.pot
	pot-create src -o $(LCAT)/messages.pot || echo "Someting unusual with pot."
	sed -i 's/\"Language: \\n/"Language: en_US\\n/g' $(LCAT)/messages.pot

init-ru:
	python setup.py init_catalog -l ru -i $(LCAT)/messages.pot -d $(LCAT)

update-ru:
	python setup.py update_catalog -l ru -i $(LCAT)/messages.pot -d $(LCAT)

comp-cat:
	python setup.py compile_catalog -d $(LCAT)

upd-cat: pot update-ru comp-cat

clean:
	$(PYTHON) setup.py clean
