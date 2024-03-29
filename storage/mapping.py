from sqlalchemy.orm import registry, relationship

from common.entities.competition import Competition
from common.entities.match import Match, MatchSet, MatchWithRelated
from common.entities.player import Player
from common.entities.player_state import PlayerState
from common.entities.ratings_state import PlayerStateSet, RatingsState
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

mapper_registry.map_imperatively(Tournament, tournaments)

mapper_registry.map_imperatively(Player, players)

mapper_registry.map_imperatively(MatchSet, sets)

mapper_registry.map_imperatively(
    Competition,
    competitions,
    properties={
        "tournament": relationship(Tournament, uselist=False),
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
    },
)

mapper_registry.map_imperatively(
    MatchWithRelated,
    matches,
    properties={
        "first_team": relationship(
            Team,
            uselist=False,
            primaryjoin="MatchWithRelated.first_team_id == Team.id",
            overlaps="first_team",
        ),
        "second_team": relationship(
            Team,
            uselist=False,
            primaryjoin="MatchWithRelated.second_team_id == Team.id",
            overlaps="second_team",
        ),
        "sets": relationship(MatchSet),
        "player_states": relationship(
            PlayerState,
            primaryjoin="MatchWithRelated.id == PlayerState.last_match_id",
        ),
    },
)

mapper_registry.map_imperatively(
    PlayerState,
    player_states,
    properties={
        "player": relationship(Player, uselist=False),
    },
)

mapper_registry.map_imperatively(
    RatingsState,
    ratings_states,
    properties={
        "player_states": relationship(
            PlayerState,
            secondary=ratings_state_player_states,
            collection_class=PlayerStateSet,
        ),
    },
)
