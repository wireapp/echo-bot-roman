docker-build:
	docker build -t lukaswire/echo-bot-roman .

docker-run: docker-build
	docker run --rm -p 8080:8080 lukaswire/echo-bot-roman

publish: docker-build
	docker push lukaswire/echo-bot-roman