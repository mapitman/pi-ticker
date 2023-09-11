default: build

build:
	docker run --privileged --rm tonistiigi/binfmt --install all
	docker buildx build --platform linux/arm/v7 -t mapitman/pi-tickerd .
restart:
	ssh $(SSH_USER)@$(TICKER_HOST) "docker stop tickerd || true"
	ssh $(SSH_USER)@$(TICKER_HOST) "docker rm tickerd || true"
	ssh $(SSH_USER)@$(TICKER_HOST) "docker run -d --privileged --name tickerd --restart always mapitman/pi-tickerd"
transfer:
	docker save mapitman/pi-tickerd | pv --size `docker inspect mapitman/pi-tickerd | jq .[0].Size` | ssh $(SSH_USER)@$(TICKER_HOST) 'docker load'
deploy: transfer restart
