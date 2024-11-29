make all:
	docker compose up -d

make clean:
	docker compose down --volumes --rmi all


make total_clean:
	docker system prune -a --volumes
