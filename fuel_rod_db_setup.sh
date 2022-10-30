#! /usr/bin/bash

pip install virtualenv
winpty python -m venv venv &&
source venv/Scripts/activate &&
pip install -r requirements.txt &&
python Fuel_Rod_DB/manage.py makemigrations fresh_inventory &&
python Fuel_Rod_DB/manage.py makemigrations temperature_excursions_exp &&
python Fuel_Rod_DB/manage.py makemigrations dry_storage_exp &&
python Fuel_Rod_DB/manage.py makemigrations temperature_excursions &&
python Fuel_Rod_DB/manage.py makemigrations dry_storage &&
python Fuel_Rod_DB/manage.py makemigrations rod_pieces &&
python Fuel_Rod_DB/manage.py migrate &&
python Fuel_Rod_DB/manage.py loaddata Fuel_Rod_DB/data.json &&
winpty python Fuel_Rod_DB/manage.py createsuperuser
