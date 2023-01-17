Migrate data from legacy ratings to local instance:
- `ssh -N -L 3306:127.0.0.1:3306 -p ${SSH_PORT} -i ~/path/to/privatekey ${SSH_HOST}
- `export PYTHONPATH=/path/to/repo/root`
- `. ./env/bin/activate`
- `python export_players.py`
- `python export_tournaments.py`
- `python 

Debug queries to compare:
```
select
      ps.ratings
    , ps.matches_played
    , ps.is_evks_rating_active
    , t1p1.last_name
    , t1p2.last_name
    , t2p1.last_name
    , t2p2.last_name
    , c.competition_type
    , t.name
from player_states ps
join matches m on ps.last_match_id = m.id
join competitions c on m.competition_id = c.id
join teams t1 on m.first_team_id = t1.id
join players t1p1 on t1.first_player_id = t1p1.id
left join players t1p2 on t1.second_player_id = t1p2.id
join teams t2 on m.second_team_id = t2.id
join players t2p1 on t2.first_player_id = t2p1.id
left join players t2p2 on t2.second_player_id = t2p2.id
join tournaments t on c.tournament_id = t.id
where ps.player_id = $player_id order by ps.id asc;
```