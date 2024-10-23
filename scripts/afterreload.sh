docker compose -f docker-compose-dev.yaml up -d --build

cd ..

cd djangoShop

poetry run python3 manage.py migrate

poetry run python3 manage.py loaddata fixtures/goods/category.json

poetry run python3 manage.py loaddata fixtures/goods/product.json

poetry run python3 manage.py createsuperuser
