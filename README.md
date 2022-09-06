`export PYTHONPATH=/local/path/to/this/repo`

```
cd this/repo
export PYTHONPATH=$(pwd)
```

pre-commit:
- `black .`
- `flake8 .`

db:
- `chmod +x core/storage/init_db/create_db.sh`
- `. core/storage/init_db/create_db.sh`
- `python core/storage/schema/create_schema.py`

console: `psql -U ratings ratings_core`