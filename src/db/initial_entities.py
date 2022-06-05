import random
from typing import List
import datetime
import uuid
import time

from src.QueryEngine import QueryEngine


class God:
    """
    utility class implementing methods that populate the database with the initial values
    """

    def __init__(self):
        self.arena_columns = ['arena_id', 'name', 'address', 'seats']
        self.arena_columns_types = ['UUID', 'text', 'text', 'list<int>']
        self.arenas = ["Uncles Iroh Arena", "Sokkas Arena", "Azulas Arena"]
        self.arenas_id = [uuid.uuid4() for _ in range(len(self.arenas))]
        self.arenas_seats = [10, 11, 12, 13]
        self.address = ['Ba Sing Se', 'Capitol City', 'Imperial City']
        self.teams = ["Dragons of the West", "Fire Ferrets", "Ba Sing Se Badgermoles", "Capital City Catgators",
                      "Laogai Lion Vultures", "Xiao Yao Zebra Frogs"]
        self.game_columns = ['game_id', 'team_1', 'team_2',
                             'arena_id', 'available_seats', 'game_date']
        self.game_columns_types = ['UUID', 'text',
                                   'text', 'UUID', 'list<int>', 'date']
        self.num_games = 10
        self.games_id = [uuid.uuid4() for _ in range(self.num_games)]
        self.query_engine = QueryEngine()

    def populate(self) -> List[str]:
        queries = [self._init_arenas(),
                   self._init_games(),
                   ]

        return queries

    def _init_arenas(self) -> str:
        query = 'BEGIN BATCH '
        for arena, arena_id, address, num_seats in zip(self.arenas, self.arenas_id, self.address, self.arenas_seats):
            seats = list(range(1, num_seats + 1))
            query += self.query_engine.insert_record(
                'arena', self.arena_columns, self.arena_columns_types, [arena_id, arena, address, seats])
        return query + " APPLY BATCH; "

    def _init_games(self):
        query = 'BEGIN BATCH '

        for idx, game_id in enumerate(self.games_id):
            team_1, team_2 = random.sample(self.teams, 2)
            arena = random.choice(list(range(len(self.arenas_id))))
            arena_id = self.arenas_id[arena]
            seats = list(range(1, self.arenas_seats[arena] + 1))

            # easy solution so that no two games will be at the same time, at the same place :)
            date = datetime.datetime.now()

            data = [game_id, team_1, team_2, arena_id, seats, date]
            query += self.query_engine.insert_record(
                'game', self.game_columns, self.game_columns_types, data)

            time.sleep(0.1)

        return query + " APPLY BATCH; "
