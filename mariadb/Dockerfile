FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=blog

COPY ./init.sql /docker-entrypoint-initdb.d/

