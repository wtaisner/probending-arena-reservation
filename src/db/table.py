from typing import List


class Table:
    arena = "CREATE TABLE IF NOT EXISTS arena (" \
            "arena_id uuid," \
            "name text," \
            "address text," \
            "seats list<int>," \
            "PRIMARY KEY(arena_id)" \
            "); "

    reservation = "CREATE TABLE IF NOT EXISTS reservation (" \
                  "reservation_id uuid," \
                  "seat_id int," \
                  "game_id uuid," \
                  "user text," \
                  "user_email text," \
                  "PRIMARY KEY(game_id, seat_id)" \
                  "); "

    game = "CREATE TABLE IF NOT EXISTS game (" \
           "game_id uuid," \
           "team_1 text," \
           "team_2 text," \
           "arena_id uuid," \
           "available_seats list<int>," \
           "game_date timestamp," \
           "PRIMARY KEY(game_id)" \
           "); "

    tables = [arena, reservation, game]

    @staticmethod
    def cleanup() -> List[str]:
        queries = ["DROP TABLE IF EXISTS arena; ",
                   "DROP TABLE IF EXISTS reservation; ",
                   "DROP TABLE IF EXISTS game; "]

        return queries
