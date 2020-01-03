PY=~/miniconda3/envs/dragnet/bin/python

serve:
	export DRAGNET_DEPLOYMENT=local \
	&& $(PY) main.py

test:
	$(PY) tests.py

clean:
	rm **/*.pyc

init:
	git submodule init \
	&& git submodule update

cloudbuild:
	gcloud builds submit --tag gcr.io/dragnet/dragnet .

deploy:
	gcloud app deploy --image-url=gcr.io/dragnet/dragnet

superdeploy: cloudbuild deploy

docker:
	docker build -t dragnet .