mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

NAME = ''

start:
	@docker compose -f docker/_testing/docker-compose-testing.yml up -d --build && docker compose -f docker/_testing/docker-compose-testing.yml start

connect_ubuntu:
	@docker exec -it molehole_testing_ubuntu_server bash

stop:
	@docker compose stop

restart: stop start

rebuild:
	@docker compose -f docker/_testing/docker-compose-testing.yml up -d --build && docker compose -f docker/_testing/docker-compose-testing.yml start
