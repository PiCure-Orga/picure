FROM python:3.9-alpine
ENV FLASK_APP "core/__init__.py"
ENV FLASK_ENV "production"
ENV FLASK_DEBUG 0

COPY / /var/www

RUN apk add g++
RUN pip install -e /var/www
RUN pip install -r /var/www/requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3","-m","flask", "run"]