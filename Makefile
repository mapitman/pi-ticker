default: build

build:
	docker build -t mapitman/pi-tickerd .
restart:
	ssh $(TICKER_HOST) "docker stop tickerd || true"
	ssh $(TICKER_HOST) "docker rm tickerd || true"
	ssh $(TICKER_HOST) "docker run -d --privileged --name tickerd --restart always mapitman/pi-tickerd"
transfer:
	docker save mapitman/pi-tickerd | pv --size `docker inspect mapitman/pi-tickerd | jq .[0].Size` | ssh $(TICKER_HOST) 'docker load'
deploy: transfer restart
	
	
	
