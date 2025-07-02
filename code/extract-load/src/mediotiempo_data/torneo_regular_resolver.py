MAX_ROUND = 17
MAX_SEASON = 2025
LEAGUES = [
    385,  # Clausura
    199,  # Apertura
]


class TorneoRegularResolver:

    def __init__(self, current_season: int, current_league: int, current_round: int):
        self.starting_season = current_season
        self.starting_league = current_league
        self.starting_round = current_round
        self._starting_league_index = LEAGUES.index(current_league)

        self._current_round = self.starting_round + 1

        if self._current_round > MAX_ROUND:
            self._current_round = 1
            self._current_league_index = (self._starting_league_index + 1) % len(LEAGUES)
            self._current_season = self.starting_season + 1
        else:
            self._current_round = self._current_round
            self._current_league_index = self._starting_league_index
            self._current_season = self.starting_season

    def _increment_round(self):
        self._current_round += 1
        if self._current_round > MAX_ROUND:
            self._current_round = 1
            self._current_league_index = (self._current_league_index + 1) % len(LEAGUES)
            self._current_season = self._current_season + 1

    def current(self):
        return self._current_season, LEAGUES[self._current_league_index], self._current_round

    def starting(self):
        return self.starting_season, LEAGUES[self._starting_league_index], self.starting_round

    def __iter__(self):
        return self  # an iterator must return itself

    def __next__(self):
        while self._current_season <= MAX_SEASON:
            result = self.current()
            self._increment_round()
            return result
        raise StopIteration
