#!/usr/bin/env bash

storage/init_db/create_db.sh
python storage/schema/create_schema.py
storage/init_db/init_db.sh