import random
from typing import List, Union, Literal

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
        self.teams = ["Dragons of the West", "Fire Ferrets"]
        self.query_engine = QueryEngine()

    def populate(self) -> List[str]:
        queries = [self._init_arenas(),
                   self._init_seats(),
                   self._init_seats(table_name='available_seat'),
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
