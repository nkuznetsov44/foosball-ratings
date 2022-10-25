curl -X POST -H "Content-Type: application/json" --data @create_players.json http://localhost:9080/api/v1/players | jq '.'
