env:
	virtualenv env

reqs:
	pip-compile -q requirements.in

bootstrap:
	pip install -r requirements.txt

build-release:
	rm -rf dist build metlo.egg-info && python setup.py sdist bdist_wheel

release:
	twine upload dist/*
