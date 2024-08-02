FROM postgres:16.0

ENV POSTGRES_DB "articles-aggregator"
ENV POSTGRES_USER "admin"
ENV POSTGRES_PASSWORD "admin"
ENV PGDATA /data/postgres

VOLUME postgres:/data/postgres
