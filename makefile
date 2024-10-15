mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

NAME = ''
CONTAINERS = molehole_testing_ubuntu_server molehole_testing_centos_server molehole_testing_debian_server molehole_testing_fedora_server molehole_testing_arch_server
start:
	@docker compose -f docker/_testing/docker-compose-testing.yml up -d --build && docker compose -f docker/_testing/docker-compose-testing.yml start

connect_python_app:
	@docker exec -it molehole_testing_python_app bash

connect_fedora:
	@docker exec -it molehole_testing_fedora_server bash

connect_arch:
	@docker exec -it molehole_testing_arch_server bash

connect_centos:
	@docker exec -it molehole_testing_centos_server bash

connect_debian:
	@docker exec -it molehole_testing_debian_server bash

connect_ubuntu:
	@docker exec -it molehole_testing_ubuntu_server bash

stop:
	@docker compose -f docker/_testing/docker-compose-testing.yml stop

restart: stop start

rebuild:
	@docker compose -f docker/_testing/docker-compose-testing.yml up -d --build && docker compose -f docker/_testing/docker-compose-testing.yml start

serve_all_backdoors:
	@echo "Starting the server on all containers..."
	@for container in $(CONTAINERS); do \
		echo "Starting server on $$container..."; \
		docker exec -d $$container /opt/sys/kernel/molehole/server; \
	done
	@echo "Servers started on all containers."

stop_all_backdoors:
	@echo "Stopping servers on all containers..."
	@for container in $(CONTAINERS); do \
		echo "Stopping server on $$container..."; \
		docker exec $$container pkill -f /opt/sys/kernel/molehole/server; \
	done
	@echo "Servers stopped on all containers."