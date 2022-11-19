from typing import ClassVar, Type
from marshmallow import fields, Schema
from marshmallow_dataclass import dataclass

from common.entities.enums import EvksPlayerRank, RatingType
from common.entities.schemas import (
    CompetitionSchema,
    TournamentSchema,
    TeamSchema,
    MatchSchema,
    PlayerSchema,
)


class PlayerResponseSchema(PlayerSchema):
    class Meta(PlayerSchema.Meta):
        fields = (
            'id',
            'first_name',
            'last_name',
            'city',
            'is_foreigner',
        )


class CompetitionResponseSchema(CompetitionSchema):
    class Meta(CompetitionSchema.Meta):
        fields = (
            'id',
            'start_datetime',
            'end_datetime',
            'competition_type',
            'evks_importance_coefficient',
            'cumulative_coefficient',
        )


class TournamentResponseSchema(TournamentSchema):
    class Meta(TournamentSchema.Meta):
        fields = (
            'id',
            'name',
            'city',
            'url',
        )


class CompetitionWithRelatedResponseSchema(CompetitionSchema):
    tournament = fields.Nested(TournamentResponseSchema)

    class Meta(CompetitionSchema.Meta):
        fields = (
            'id',
            'start_datetime',
            'end_datetime',
            'competition_type',
            'evks_importance_coefficient',
            'cumulative_coefficient',
            'tournament',
        )


class TeamResponseSchema(TeamSchema):
    first_player = fields.Nested(PlayerResponseSchema)
    second_player = fields.Nested(PlayerResponseSchema)

    class Meta(TeamSchema.Meta):
        fields = (
            'id',
            'competition_place',
            'competition_order',
            'first_player',
            'second_player',
        )


class MatchResponseSchema(MatchSchema):
    first_team = fields.Nested(TeamResponseSchema)
    second_team = fields.Nested(TeamResponseSchema)

    class Meta(MatchSchema.Meta):
        fields = (
            'id',
            'first_team',
            'second_team',
            'start_datetime',
            'end_datetime',
            'force_qualification',
            'is_forfeit',
            'grand_final_options',
        )


@dataclass
class PlayerStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    player_id: int
    player_name: str
    evks_rank: EvksPlayerRank
    rating: int
    is_evks_player_active: bool


class PlayerCompetitionMatchesResponseSchema(MatchResponseSchema):
    # player_state = fields.Nested(PlayerStateResponseSchema)  # FIXME
    pass


@dataclass
class RatingsStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    id: int
    rating_type: RatingType
    player_states: list[PlayerStateResponse]
