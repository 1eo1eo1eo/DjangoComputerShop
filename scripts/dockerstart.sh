#!/bin/sh

cd djangoShop

poetry run python3 manage.py migrate

poetry run python3 manage.py loaddata fixtures/goods/category.json

poetry run python3 manage.py loaddata fixtures/goods/product.json

poetry run python3 manage.py loaddata fixtures/users/users.json

poetry run pytest --maxfail=1 -v

poetry run python3 manage.py runserver 0.0.0.0:8000