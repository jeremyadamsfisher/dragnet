# adapted from https://issuetracker.google.com/issues/129913216

FROM gcr.io/google-appengine/python
RUN virtualenv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt ./requirements.txt
RUN pip3 install -r  ./requirements.txt \
               && rm ./requirements.txt

ADD secrets.json .env ./

ADD . /app
CMD gunicorn -b :$PORT main:app