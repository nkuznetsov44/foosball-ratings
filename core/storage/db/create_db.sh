#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cat ${BASEDIR}/create_db.sql | psql