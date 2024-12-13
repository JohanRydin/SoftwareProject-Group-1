
.PHONY: test

 up:
	docker compose up -d

 down: 
	docker compose down

 clean:
	docker compose down --volumes --rmi all


 total_clean:
	docker system prune -a --volumes

 test: 
	cd fastAPI && pytest
