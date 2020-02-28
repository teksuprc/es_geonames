SHELL := /bin/bash

up:
	docker-compose up -d

down:
	docker-compose down

geonames:
	docker-compose up -d
	curl https://download.geonames.org/export/dump/allCountries.zip --output allCountries.zip
	unzip allCountries -d ${PWD}/data/geonames
	python ${PWD}/geonames_es_loader.py 
