`export PYTHONPATH=/local/path/to/this/repo`

pre-commit:
- `black .`
- `flake8 .`

db:
```
create database ratings_core;
create user ratings with encrypted password 'ratings';
grant all privileges on database ratings_core to ratings;
```

`cat core/storage/db/schema/init_schema.sql | psql -U ratings ratings_core`

console: `psql -U ratings ratings_core`