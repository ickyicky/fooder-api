# builder
FROM python:3.11.5-bullseye as builder

RUN mkdir /opt/fooder
WORKDIR /opt/fooder

RUN pip install setuptools

COPY fooder /opt/fooder/fooder
COPY setup.py /opt/fooder/setup.py

RUN python /opt/fooder/setup.py sdist
RUN mv /opt/fooder/dist/FooderApi*.tar.gz /opt/fooder/dist/fooder.tar.gz

# final image
FROM python:3.11.5-bullseye

RUN apt-get -y install libpq-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN useradd fooder

RUN mkdir /opt/fooder && chown fooder:fooder /opt/fooder
WORKDIR /opt/fooder

COPY --from=builder /opt/fooder/dist/fooder.tar.gz /opt/fooder/fooder.tar.gz
RUN pip install fooder.tar.gz
RUN rm fooder.tar.gz

CMD ["uvicorn", "fooder.app:app", "--host", "0.0.0.0", "--port", "8000"]
