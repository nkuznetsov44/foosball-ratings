from typing import ClassVar, Type, Optional
from dataclasses import field
from marshmallow import fields, Schema
from marshmallow_dataclass import dataclass as mm_dataclass

from common.entities.enums import EvksPlayerRank, RatingType
from common.entities.team import Team
from common.entities.match import MatchSet, GrandFinalOptions
from common.entities.schemas import (
    CompetitionSchema,
    TournamentSchema,
    TeamSchema,
    MatchSetSchema,
    PlayerSchema,
)


class PlayerResponseSchema(PlayerSchema):
    class Meta(PlayerSchema.Meta):
        fields = (
            "id",
            "first_name",
            "last_name",
            "city",
            "is_foreigner",
        )


@mm_dataclass
class PlayerStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    player_id: int
    player_name: str
    evks_rank: EvksPlayerRank
    rating: int
    is_evks_player_active: bool


@mm_dataclass
class RatingsStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    id: int
    rating_type: RatingType
    player_states: list[PlayerStateResponse]


@mm_dataclass
class ExternalPlayerStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    player: PlayerResponseSchema = field(
        metadata=dict(
            marshmallow_field=fields.Nested(PlayerResponseSchema)
        )
    )
    evks_rank: EvksPlayerRank
    rating: int
    is_evks_player_active: bool


@mm_dataclass
class ExternalRatingsStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    player_states: list[ExternalPlayerStateResponse]


class MatchSetResponseSchema(MatchSetSchema):
    class Meta(MatchSetSchema.Meta):
        fields = (
            "id",
            "order",
            "first_team_score",
            "second_team_score",
        )


class TeamResponseSchema(TeamSchema):
    first_player = fields.Nested(PlayerResponseSchema)
    second_player = fields.Nested(PlayerResponseSchema)

    class Meta(TeamSchema.Meta):
        fields = (
            "id",
            "competition_place",
            "competition_order",
            "first_player",
            "second_player",
        )


@mm_dataclass
class MatchPlayerStateResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    id: int
    player_id: int
    evks_rank: EvksPlayerRank
    ratings: dict[RatingType, int]
    is_evks_player_active: bool


@mm_dataclass
class MatchWithRelatedResponse:
    Schema: ClassVar[Type[Schema]] = Schema

    id: int
    first_team: Team = field(
        metadata=dict(marshmallow_field=fields.Nested(TeamResponseSchema))
    )
    second_team: Team = field(
        metadata=dict(marshmallow_field=fields.Nested(TeamResponseSchema))
    )
    is_qualification: bool
    is_forfeit: Optional[bool]
    grand_final_options: Optional[GrandFinalOptions]
    sets: list[MatchSet] = field(
        metadata=dict(
            marshmallow_field=fields.Nested(MatchSetResponseSchema, many=True)
        )
    )
    player_states: list[MatchPlayerStateResponse]


class CompetitionResponseSchema(CompetitionSchema):
    class Meta(CompetitionSchema.Meta):
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "competition_type",
            "evks_importance_coefficient",
            "cumulative_coefficient",
        )


class TournamentResponseSchema(TournamentSchema):
    class Meta(TournamentSchema.Meta):
        fields = (
            "id",
            "name",
            "city",
            "url",
        )


class CompetitionWithRelatedResponseSchema(CompetitionSchema):
    tournament = fields.Nested(TournamentResponseSchema)

    class Meta(CompetitionSchema.Meta):
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "competition_type",
            "evks_importance_coefficient",
            "cumulative_coefficient",
            "tournament",
        )
