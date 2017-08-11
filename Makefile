.PHONY: build
build:
	python setup.py install

.PHONY: test
test:
	nosetests -v -s --with-coverage --cover-xml-file=coverage.xml --cover-xml  
	cd docs && make html
