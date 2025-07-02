up:
	docker-compose up --build

down:
	docker-compose down -v

images:
	docker build -t localhost:5001/dbt_futbol -f dbt/Dockerfile dbt
	docker push localhost:5001/dbt_futbol
	docker build -t localhost:5001/python_futbol -f python/Dockerfile python
	docker push localhost:5001/python_futbol

