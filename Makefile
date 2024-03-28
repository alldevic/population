#!/usr/bin/make

#include .env

SHELL = /bin/sh
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID

BACKEND_CONTAINER = population

export BACKEND_CONTAINER

up:
	docker volume create postgres
	docker volume create pgadmin
	docker volume create upload
	docker compose up -d --build --remove-orphans 
down:
	docker compose down
sh:
	docker exec -it /$(BACKEND_CONTAINER) /bin/bash
logsb:
	docker logs /$(BACKEND_CONTAINER) -f
logs:
	docker compose logs -f
