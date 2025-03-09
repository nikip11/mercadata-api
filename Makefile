build:
	docker-compose up --build --remove-orphans
up:
	docker-compose up --remove-orphans
sh:
	docker-compose run app sh