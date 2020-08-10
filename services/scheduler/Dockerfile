FROM python:3.8.2-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5070

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "wsgi:app"]