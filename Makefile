PY=~/miniconda3/envs/dragnet/bin/python

serve:
	export DRAGNET_DEBUG=1 && $(PY) run.py
test:
	$(PY) tests.py
clean:
	rm **/*.pyc