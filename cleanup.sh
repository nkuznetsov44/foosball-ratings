#!/usr/bin/env bash

core/storage/init_db/create_db.sh
python core/storage/db/schema/create_schema.py