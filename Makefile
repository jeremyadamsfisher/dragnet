PY=~/miniconda3/envs/dragnet/bin/python
DOCKER_IMG     =gcr.io/dragnet/dragnet
DOCKER_IMG_BASE=gcr.io/dragnet/dragnet-base

serve:
	export DRAGNET_DEPLOYMENT=local \
	&& $(PY) main.py

test:
	$(PY) tests.py

clean:
	rm **/*.pyc

init:
	git submodule init \
	&& git submodule update \
	&& docker pull $(DOCKER_IMG_BASE)

buildbase:
	docker build -t $(DOCKER_IMG_BASE) \
			     --target base . \
	&& docker push $(DOCKER_IMG_BASE)

build: buildbase
	docker build -t $(DOCKER_IMG) . \
		--cache-from $(DOCKER_IMG_BASE) \

deploy: build
	docker push $(DOCKER_IMG):latest \
	&& gcloud app deploy --image-url=$(DOCKER_IMG)