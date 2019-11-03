PY=~/miniconda3/envs/dragnet/bin/python

serve:
	$(PY) run.py
test:
	$(PY) tests.py
clean:
	rm **/*.pyc