from dataclasses import dataclass


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
