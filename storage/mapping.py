from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from common.entities.competition import Competition
from common.entities.match import Match, MatchSet
from common.entities.player import Player
from common.entities.state import PlayerState, RatingsState
from common.entities.team import Team
from common.entities.tournament import Tournament
from storage.tables import (
    competitions,
    matches,
    player_states,
    players,
    ratings_state_player_states,
    ratings_states,
    sets,
    teams,
    tournaments,
)

mapper_registry = registry()

mapper_registry.map_imperatively(
    Competition,
    competitions,
    properties={
        "matches": relationship(Match),
        "teams": relationship(Team),
    },
)

mapper_registry.map_imperatively(
    Match,
    matches,
    properties={
        "first_team": relationship(
            Team,
            uselist=False,
            primaryjoin="Match.first_team_id == Team.id",
        ),
        "second_team": relationship(
            Team,
            uselist=False,
            primaryjoin="Match.second_team_id == Team.id",
        ),
        "sets": relationship(MatchSet),
    },
)

mapper_registry.map_imperatively(MatchSet, sets)

mapper_registry.map_imperatively(Player, players)

mapper_registry.map_imperatively(
    PlayerState,
    player_states,
    properties={
        "player": relationship(Player, uselist=False),
        "last_match": relationship(Match, uselist=False),
    },
)

mapper_registry.map_imperatively(
    RatingsState,
    ratings_states,
    properties={
        "player_states": relationship(
            PlayerState,
            secondary=ratings_state_player_states,
            collection_class=attribute_mapped_collection("player_id"),
        ),
        "last_competition": relationship(Competition, uselist=False),
    },
)

mapper_registry.map_imperatively(
    Team,
    teams,
    properties={
        "first_player": relationship(
            Player, uselist=False, primaryjoin="Team.first_player_id == Player.id"
        ),
        "second_player": relationship(
            Player, uselist=False, primaryjoin="Team.second_player_id == Player.id"
        ),
    },
)

mapper_registry.map_imperatively(
    Tournament,
    tournaments,
    properties={
        "competitions": relationship(Competition),
    },
)
