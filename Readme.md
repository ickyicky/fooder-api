# FOODER

Simple API for food diary application. It uses FastAPI and async postgres.

## Usage

Simply build docker images with:

```bash
docker-compose build
```

And then start them up with:

```bash
docker-compose up -d
```

Create `.env` file with configuration by copying template `env.template`. *You have to generate secret keys!* They are stored under `SECRET_KEY` and `REFRESH_SECRET_KEY`
in `.env` file and both could be generated with `openssl rand -hex 32`.

To initialize database exec:

```bash
docker-compose exec api bash -c python -m fooder --create-tables
```

## Deployment

For deployment delete:

```
    volumes:
      - ./fooder:/opt/fooder/fooder
```

and

```
    command: "uvicorn fooder.app:app --host 0.0.0.0 --port 8000 --reload"
```

lines from `docker-compose.yml`. This line makes app reload everytime code changes and is only recommended for development purposes.

I highly recommend using reverse proxy like nginx for HTTPS.

## Documentation

When api is started using docker, by default it runs on 8000 port on local machine (it can be changed within `docker-compose.yml` file). Swagger documentation is available
on `http://0.0.0.0:8000/docs` when you start the app.

Alternatively you can visit [my own instance of the API docs](https://fooderapi.domandoman.xyz/docs).
