import random
from typing import List

import uuid


class God:
    """
    utility class implementing methods that populate the database with the initial values
    """

    def __init__(self):
        self.arenas = ["Uncles Iroh Arena", "Sokkas Arena"]
        self.arenas_id = [uuid.uuid4() for _ in range(len(self.arenas))]
        self.address = ['Ba Sing Se', 'Capitol City']
        self.teams = ["Dragons of the West", "Fire Ferrets"]

    def populate(self) -> List[str]:
        queries = [self._init_arenas(), self._init_seats()]

        # TODO: add next initializations

        return queries

    def _init_arenas(self) -> str:
        query = 'BEGIN BATCH '
        for arena, arena_id, address in zip(self.arenas, self.arenas_id, self.address):
            # arena_id = uuid.uuid4()
            query += "INSERT INTO arena (arena_id, name, address) VALUES " \
                     + f"('{arena_id}', '{arena}', '{address}');"
            # self.arenas_id.append(arena_id)
        return query + " APPLY BATCH; "

    def _init_seats(self) -> str:
        query = 'BEGIN BATCH '
        for arena_id in self.arenas_id:
            seat_id = [uuid.uuid4() for _ in range(10)]
            for idx in seat_id:
                query += "INSERT INTO seat (seat_id, arena_id) VALUES " \
                         + f"('{idx}', '{arena_id}');"

        return query + " APPLY BATCH; "
