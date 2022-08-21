`export PYTHONPATH=/local/path/to/this/repo`

pre-commit:
- `black .`
- `flake8 .`

db:
- `chmod +x ./core/storage/db/create_db.sh`
- `./core/storage/db/create_db.sh`
- `python core/storage/db/schema/create_schema.py`

console: `psql -U ratings ratings_core`