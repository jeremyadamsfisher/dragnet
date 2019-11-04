PY=~/miniconda3/envs/dragnet/bin/python

serve:
	export DRAGNET_DEBUG=1 && $(PY) main.py
test:
	$(PY) tests.py
clean:
	rm **/*.pyc

cloudbuild:
	gcloud builds submit --tag gcr.io/dragnet/dragnet .

deploy:
	gcloud app deploy --image-url=gcr.io/dragnet/dragnet

superdeploy: cloudbuild deploy