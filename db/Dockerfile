FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=storage

COPY ./blueprint.sql /docker-entrypoint-initdb.d/

EXPOSE 3307:3306

