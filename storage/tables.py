import sqlalchemy as sa

from common.entities.enums import (
    City,
    CompetitionType,
    EvksPlayerRank,
    RatingsStateStatus,
)
from storage.types import RatingsJSON, GrandFinalOptionsJSON

metadata_obj = sa.MetaData()


competitions = sa.Table(
    "competitions",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("external_id", sa.Integer, nullable=True),
    sa.Column("tournament_id", sa.Integer, sa.ForeignKey("tournaments.id")),
    sa.Column("competition_type", sa.Enum(CompetitionType)),
    sa.Column("order", sa.Integer),
    sa.Column("evks_importance_coefficient", sa.Numeric),
    sa.Column("cumulative_coefficient", sa.Numeric),
    sa.Column("start_datetime", sa.DateTime(timezone=True)),
    sa.Column("end_datetime", sa.DateTime(timezone=True)),
    sa.UniqueConstraint("tournament_id", "external_id"),
)

sets = sa.Table(
    "sets",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("external_id", sa.Integer, nullable=True),
    sa.Column("match_id", sa.Integer, sa.ForeignKey("matches.id")),
    sa.Column("order", sa.Integer),
    sa.Column("first_team_score", sa.Integer),
    sa.Column("second_team_score", sa.Integer, nullable=True),
    sa.UniqueConstraint("match_id", "external_id"),
    sa.UniqueConstraint("match_id", "order"),
)

matches = sa.Table(
    "matches",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("external_id", sa.Integer, nullable=True),
    sa.Column("competition_id", sa.Integer, sa.ForeignKey("competitions.id")),
    sa.Column("order", sa.Integer()),
    sa.Column("first_team_id", sa.Integer, sa.ForeignKey("teams.id")),
    sa.Column("second_team_id", sa.Integer, sa.ForeignKey("teams.id")),
    sa.Column("start_datetime", sa.DateTime(timezone=True)),
    sa.Column("end_datetime", sa.DateTime(timezone=True)),
    sa.Column("force_qualification", sa.Boolean),
    sa.Column("is_forfeit", sa.Boolean),
    sa.Column("grand_final_options", GrandFinalOptionsJSON),
    sa.UniqueConstraint("competition_id", "external_id"),
    sa.UniqueConstraint("competition_id", "order"),
)

players = sa.Table(
    "players",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("external_id", sa.Integer, nullable=True),
    sa.Column("first_name", sa.String(255)),
    sa.Column("last_name", sa.String(255)),
    sa.Column("city", sa.Enum(City)),
    sa.Column("is_foreigner", sa.Boolean),
)

player_states = sa.Table(
    "player_states",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column(
        "previous_state_id",
        sa.Integer,
        sa.ForeignKey("player_states.id"),
        nullable=True,
    ),
    sa.Column("player_id", sa.Integer, sa.ForeignKey("players.id")),
    sa.Column("matches_played", sa.Integer),
    sa.Column("matches_won", sa.Integer),
    sa.Column("last_match_id", sa.Integer, sa.ForeignKey("matches.id")),
    sa.Column("ratings", RatingsJSON),
    sa.Column("evks_rank", sa.Enum(EvksPlayerRank)),
    sa.Column("is_evks_rating_active", sa.Boolean),
)

ratings_state_player_states = sa.Table(
    "ratings_state_player_states",
    metadata_obj,
    sa.Column("player_state_id", sa.ForeignKey("player_states.id")),
    sa.Column("ratings_state_id", sa.ForeignKey("ratings_states.id")),
)

ratings_states = sa.Table(
    "ratings_states",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column(
        "previous_state_id",
        sa.Integer,
        sa.ForeignKey("ratings_states.id"),
        nullable=True,
    ),
    sa.Column("last_competition_id", sa.Integer, sa.ForeignKey("competitions.id")),
    sa.Column("status", sa.Enum(RatingsStateStatus)),
)

teams = sa.Table(
    "teams",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("competition_id", sa.Integer, sa.ForeignKey("competitions.id")),
    sa.Column("external_id", sa.Integer, nullable=True),
    sa.Column("competition_place", sa.Integer),
    sa.Column("competition_order", sa.Integer),
    sa.Column("first_player_id", sa.Integer, sa.ForeignKey("players.id")),
    sa.Column(
        "second_player_id", sa.Integer, sa.ForeignKey("players.id"), nullable=True
    ),
    sa.UniqueConstraint("competition_id", "external_id"),
)

tournaments = sa.Table(
    "tournaments",
    metadata_obj,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("external_id", sa.Integer, nullable=True, unique=True),
    sa.Column("name", sa.String(255)),
    sa.Column("city", sa.Enum(City)),
    sa.Column("url", sa.String(511), nullable=True),
)
