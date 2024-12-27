.PHONY: build up down attach bash shell migrate migrations
update-deps:
	pip install -U pip && pip install pip-tools

	pip-compile requirements/base.in
	pip-compile requirements/dev.in


build:
	[ -f .env ] || cp example.env .env
	docker compose build

up:
	make build
	docker compose up

down:
	docker compose down

# For debbuging
attach:
	docker attach django_app

bash:
	docker exec -it django_app bash

shell:
	docker exec -it django_app python manage.py shell

migrate:
	docker exec -it django_app python manage.py migrate

migrations:
	docker exec -it django_app python manage.py makemigrations

createsuperuser:
	docker exec -it django_app python manage.py createsuperuser

dropdatabase:
	docker exec -it db psql -U postgres -c "DROP DATABASE IF EXISTS mydatabase;"
	docker exec -it db psql -U postgres -c "CREATE DATABASE mydatabase;"
