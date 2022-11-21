Deploy local database:
- `create database ratings_core`
- create user `ratings` and grants if needed:
    ```
    GRANT USAGE ON SCHEMA public TO ratings;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ratings;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to ratings;
    ```
- `psql -U ratings ratings_core < storage/schema/dumps/ab2e2d3b29fe53ac44d9eeffe615e6ad779030aa.sql`
- `psql -U ratings ratings_core < storage/init_db/init_db.sql`