Dump data from legacy ratings

1. Players
```
python3 -m venv env
. ./env/bin/activate
python3 -m pip install -r requirements.txt

export PYTHONPATH=/path/to/repo/root

# proxy legacy mysql database port to localhost
python3 generate_create_players.py > create_players.json

./create_players.sh
```