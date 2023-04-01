from python

RUN apt-get -y install libpq-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /opt/fooder
WORKDIR /opt/fooder

COPY fooder /opt/fooder/fooder

CMD ["uvicorn", "fooder.app:app", "--host", "0.0.0.0", "--port", "8000"]
