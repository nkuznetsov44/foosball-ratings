#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cat ${BASEDIR}/init_db.sql | psql -U ratings ratings_core