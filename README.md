`export PYTHONPATH=/local/path/to/this/repo`

```
cd this/repo
export PYTHONPATH=$(pwd)
```

pre-commit:
- `black .`
- `flake8 .`

Docker build and run locally: `docker-compose -f docker-compose.build-local.yml up --build`

Run core without docker:
- `. ./env/bin/activate`
- deploy database:
    - `cd storage && docker-compose up -d`
    - `python3 schema/create_schema.py`
    - `cat ./init_db/init_db.sql | docker exec storage-postgres-1 psql -U ratings -d ratings_core`
- `python3 core/application.py`
- if needed upload testing data or data from legacy ratings via api