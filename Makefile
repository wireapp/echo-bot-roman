docker-build:
	docker build -t lukaswire/echo-bot-roman .

docker-run:
	docker run --rm -p 8080:8080 lukaswire/echo-bot-roman

docker-deploy:
	docker push lukaswire/echo-bot-roman