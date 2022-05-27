import random
from typing import List, Literal
import datetime
import uuid

from src.QueryEngine import QueryEngine


class God:
    """
    utility class implementing methods that populate the database with the initial values
    """

    def __init__(self):
        self.arena_columns = ['arena_id', 'name', 'address']
        self.arena_columns_types = ['UUID', 'text', 'text']
        self.seats_columns = ['seat_id', 'arena_id']
        self.seats_columns_types = ['UUID', 'UUID']
        self.arenas = ["Uncles Iroh Arena", "Sokkas Arena", "Azulas Arena"]
        self.arenas_id = [uuid.uuid4() for _ in range(len(self.arenas))]
        self.address = ['Ba Sing Se', 'Capitol City', 'Imperial City']
        self.teams = ["Dragons of the West", "Fire Ferrets", "Ba Sing Se Badgermoles", "Capital City Catgators",
                      "Laogai Lion Vultures", "Xiao Yao Zebra Frogs"]
        self.game_columns = ['game_id', 'team_1', 'team_2', 'arena_id', 'game_date']
        self.game_columns_types = ['UUID', 'text', 'text', 'UUID', 'date']
        self.query_engine = QueryEngine()

    def populate(self) -> List[str]:
        num_seats = 10  # <- change if you want more seats per arena
        queries = [self._init_arenas(),
                   self._init_seats(num_seats=num_seats),
                   self._init_seats(num_seats=num_seats, table_name='available_seat'),
                   self._init_games(),
                   ]

        # TODO: add next initializations

        return queries

    def _init_arenas(self) -> str:
        query = 'BEGIN BATCH '
        for arena, arena_id, address in zip(self.arenas, self.arenas_id, self.address):
            query += self.query_engine.insert_record(
                'arena', self.arena_columns, self.arena_columns_types, [arena_id, arena, address])
        return query + " APPLY BATCH; "

    def _init_seats(self, num_seats: int = 10, table_name: Literal['seat', 'available_seat'] = 'seat') -> str:
        query = 'BEGIN BATCH '
        for arena_id in self.arenas_id:
            seat_id = [uuid.uuid4() for _ in range(num_seats)]
            for idx in seat_id:
                query += self.query_engine.insert_record(
                    table_name, self.seats_columns, self.seats_columns_types, [idx, arena_id])

        return query + " APPLY BATCH; "

    def _init_games(self, num_games: int = 10):
        query = 'BEGIN BATCH '
        games_id = [uuid.uuid4() for _ in range(num_games)]
        for idx, game_id in enumerate(games_id):
            team_1, team_2 = random.sample(self.teams, 2)
            arena_id = random.sample(self.arenas_id, 1)[0]

            # easy solution so that no two games will be at the same time, at the same place :)
            date = datetime.datetime.now()

            data = [game_id, team_1, team_2, arena_id, date]
            query += self.query_engine.insert_record('game', self.game_columns, self.game_columns_types, data)

        return query + " APPLY BATCH; "
