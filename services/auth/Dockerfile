FROM python:3.8.2-slim-buster

VOLUME ["/app"]

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5090

#CMD ["gunicorn", "--certfile", "cert.pem", "--keyfile", "key.pem", "--config", "gunicorn-cfg.py", "wsgi:app"]
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "wsgi:app"]