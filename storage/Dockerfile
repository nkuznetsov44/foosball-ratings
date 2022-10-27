FROM postgres

COPY ./schema/dumps/60cd355b24689707134c98fe44ac3be6a06f26a6.sql /docker-entrypoint-initdb.d/1-schema.sql
COPY ./init_db/init_db.sql /docker-entrypoint-initdb.d/2-init_db.sql