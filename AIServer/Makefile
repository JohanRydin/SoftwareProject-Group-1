build_docker:
	docker build -t recommendations-fastapi .

run_docker:
	docker run -d --name recommendations -p 5000:5000 recommendations-fastapi

restart_docker:
	docker restart recommendations

clean_docker:
	docker rm recommendations
	docker image rm recommendations-fastapi

stop_docker:
	docker stop recommendations
