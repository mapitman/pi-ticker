default: build

build:
	docker build -t mapitman/pi-tickerd .

deploy:
	docker save mapitman/pi-tickerd | bzip2 | pv | ssh $(TICKER_HOST) 'bunzip2 | docker load'
	ssh $(TICKER_HOST) "docker stop tickerd"
	ssh $(TICKER_HOST) "docker rm tickerd"
	ssh $(TICKER_HOST) "docker run -d --privileged --name tickerd --restart unless-stopped mapitman/pi-tickerd"
