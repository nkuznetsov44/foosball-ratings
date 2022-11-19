Migrate data from legacy ratings to local instance:
- `ssh -N -L 3306:127.0.0.1:3306 -p ${SSH_PORT} -i ~/path/to/privatekey ${SSH_HOST}
- `export PYTHONPATH=/path/to/repo/root`
- `python export_players.py | jq '.'`
- `python export_tournaments.py`
- `python 