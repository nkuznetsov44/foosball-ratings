## Pre-commit
- `black -l 100 .`
- `flake8 .`

## Build and run locally in Docker
- `docker-compose -f docker-compose.build-local.yml up --build`
  Now you have your core app on port 9080 and webapp on port 9081

## How to upload test data
- Upload players: `curl -X POST -H "Content-Type: application/json" --data "@$(pwd)/storage/test_data/players.json" http://localhost:9080/api/v1/players | jq '.'`
- Upload tournament:
  ```
  TOURNAMENT_ID=$(curl -X POST -H "Content-Type: application/json" \
  --data "@$(pwd)/storage/test_data/tournament.json" \
  http://localhost:9080/api/v1/tournaments | jq '.id' --raw-output)
  ```
- Upload OS:
  ```
  curl -X POST -H "Content-Type: application/json" \
    --data "@$(pwd)/storage/test_data/competition_singles.json" \
    "http://localhost:9080/api/v1/tournaments/${TOURNAMENT_ID}/competitions" | jq '.'`
  ```
- Upload OD:
  ```
  curl -X POST -H "Content-Type: application/json" \
    --data "@$(pwd)/storage/test_data/competition_doubles.json" \
    "http://localhost:9080/api/v1/tournaments/${TOURNAMENT_ID}/competitions" | jq '.'`
  ```

## Run locally without docker

### Python venv
- If you dont have an existing env, create it `python3 -m venv env`
- Activate the environment `. ./env/bin/activate`
- If needed install requirements `python3 -m pip install -r requirements.dev.txt`
- Set PYTHONPATH variable `export PYTHONPATH=$(pwd)`

### Core
- deploy database:
    - `cd storage && docker-compose up -d`
    - `python3 schema/create_schema.py`
    - `cat ./init_db/init_db.sql | docker exec storage-postgres-1 psql -U ratings -d ratings_core`
- `python3 core/application.py`

### Webapp
- `python3 webapp/application.py`curl -X POST -H "Content-Type: application/json" --data "@$(pwd)/storage/test_data/players.json" http://localhost:9080/v1/players | jq '.'

## Environment
- WEBAPP_BACKEND_URL needed to run frontend in docker

## Testing
- `pytest .`
