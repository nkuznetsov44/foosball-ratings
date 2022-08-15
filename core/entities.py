from typing import Optional
from dataclasses import dataclass
from datetime import date, datetime


# Для read-копии идея такая:
#
# Есть current_state, из него достаем list(PlayerState) - актуальные рейтинги игроков
# И турниры берем только те (условно), у которых id < last_competition_id
#
# Таким образом у нас в read-слое всегда актуальное состояние, нет грязных данных
# А новые туда попадут после окончательной обработки CreateCompetitionEvent и вызова flush_state(new_state: RatingState)


@dataclass(frozen=True)
class Player:
    id: int
    first_name: str
    last_name: str
    sex: str


@dataclass(frozen=True)
class MatchSet:
    first_player_score: int
    second_player_score: int

    @property
    def is_first_player_win(self) -> bool:
        return self.first_player_score > self.second_player_score


@dataclass(frozen=True)
class Match:
    id: int
    first_player: Player
    second_player: Player
    sets: list[MatchSet]
    start_time: datetime
    end_time: datetime

    @property
    def first_player_sets_score(self) -> int:
        return len(filter(MatchSet.is_first_player_win, self.sets))
    
    @property
    def second_player_sets_score(self) -> int:
        return len(self.sets) - self.first_player_sets_score

    @property
    def is_first_player_win(self) -> bool:
        return self.first_player_sets_score > self.second_player_sets_score


@dataclass(frozen=True)
class Competition:
    id: int
    matches: list[Match]


@dataclass(frozen=True)
class PlayerState:
    """Описывает состояние рейтинга игрока в момент времени, после истории сыгранных к этому моменту матчей."""
    id: int
    player: Player
    last_match: Optional[Match]  # optional for players initial state where no matches were played
    rating: int


@dataclass
class RatingState:
    """
    Описывает состояние рейтинга в момент времени, после обработки истории турниров, сыгранных к этому моменту.
    Состоит из состояний игроков после окончательной обработки категории.
    """
    id: Optional[int]  # None for dirty state
    player_states: set[PlayerState]
    last_competition_id: Optional[Competition]  # optional for initial state where no competition were played

    def lookup_player_state(self, player: Player) -> Optional[PlayerState]:
        return next(filter(lambda ps: ps.player.id == player.id, self.player_states), None)
