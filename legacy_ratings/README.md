Dump data from legacy ratings

1. Players
```
python3 -m venv env
. ./env/bin/activate
python3 -m pip install -r requirements.txt

export PYTHONPATH=/path/to/repo/root

# proxy legacy mysql database port to localhost
python3 export_players.py > players.json

curl -X POST -H "Content-Type: application/json" --data @players.json http://localhost:9080/api/v1/players | jq '.'
```