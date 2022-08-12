from typing import Optional
from dataclasses import dataclass
from storage.model import Player, Match, Competition


# Для read-копии идея такая:
#
# Есть current_state, из него достаем list(PlayerState) - актуальные рейтинги игроков
# И турниры берем только те (условно), у которых id < last_competition_id
#
# Таким образом у нас в read-слое всегда актуальное состояние, нет грязных данных
# А новые туда попадут после окончательной обработки CreateCompetitionEvent и вызова flush_state(new_state: RatingState)


@dataclass
class PlayerState:
    player: Player
    last_match: Optional[Match]  # optional for players initial state where no matches were played
    rating: int


@dataclass
class RatingState:
    player_states: set[PlayerState]
    last_competition_id: Optional[Competition]  # optional for initial state where no competition were played

    def lookup_player_state(self, Player) -> PlayerState:
        # looks up player state from rating state
        pass
