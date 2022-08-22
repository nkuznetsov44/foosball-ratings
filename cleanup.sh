#!/usr/bin/env bash

./core/storage/db/create_db.sh
python core/storage/db/schema/create_schema.py