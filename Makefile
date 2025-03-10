build:
	docker-compose up --build --remove-orphans
up:
	docker-compose up --remove-orphans
sh:
	docker-compose run app sh

drun:
	docker build -t app_py1 . && docker rm app_py1 && docker run -it --name app_py1 -w /app app_py1
