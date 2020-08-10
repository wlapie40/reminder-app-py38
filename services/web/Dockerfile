FROM python:3.8.2-slim-buster

WORKDIR /web

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY . /web

#RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5060

#CMD ["gunicorn", "--certfile", "cert.pem", "--keyfile", "key.pem", "--config", "gunicorn-cfg.py", "wsgi:app"]
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "wsgi:app"]