curl -X POST -H "Content-Type: application/json" --data @players.json http://localhost:9080/api/v1/players | jq '.'
curl -X POST -H "Content-Type: application/json" --data @tournament.json http://localhost:9080/api/v1/tournaments | jq '.'