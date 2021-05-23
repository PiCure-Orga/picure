FROM python:3.9-alpine
ENV FLASK_APP "core/__init__.py"
ENV FLASK_ENV "production"
ENV FLASK_DEBUG 0

COPY / /var/www

RUN apk add g++
WORKDIR /var/www
RUN pip install .
RUN pip install gunicorn

EXPOSE 5000

ENTRYPOINT ["gunicorn","-w","2","-b","0.0.0.0:5000","picure:create_app()"]
