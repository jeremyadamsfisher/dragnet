# adapted from https://issuetracker.google.com/issues/129913216

FROM gcr.io/google-appengine/python as base
RUN virtualenv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt ./requirements.txt
RUN pip3 install -r  ./requirements.txt \
               && rm ./requirements.txt


# replace with `FROM base` to build from scratch
FROM gcr.io/dragnet/dragnet-base

ADD secrets.json ./
ADD . /app
CMD export DRAGNET_DEPLOYMENT="production" \
    && gunicorn -b :$PORT main:app