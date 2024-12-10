
.PHONY: test

make up:
	docker compose up -d

make down: 
	docker compose down

make clean:
	docker compose down --volumes --rmi all


make total_clean:
	docker system prune -a --volumes

make test: 
	cd fastAPI && pytest
