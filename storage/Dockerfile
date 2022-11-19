FROM postgres

COPY ./schema/dumps/ab2e2d3b29fe53ac44d9eeffe615e6ad779030aa.sql /docker-entrypoint-initdb.d/1-schema.sql
COPY ./init_db/init_db.sql /docker-entrypoint-initdb.d/2-init_db.sql