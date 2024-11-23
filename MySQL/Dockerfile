FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=gamehive
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

COPY ./blueprint.sql /docker-entrypoint-initdb.d/

EXPOSE 3307:3306

