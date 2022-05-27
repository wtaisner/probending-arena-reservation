from typing import List


class Table:
    arena = "CREATE TABLE IF NOT EXISTS arena (" \
            "arena_id text," \
            "name text," \
            "address text," \
            "PRIMARY KEY(arena_id)" \
            "); "

    seat = "CREATE TABLE IF NOT EXISTS seat (" \
           "seat_id text," \
           "arena_id text," \
           "PRIMARY KEY(seat_id, arena_id)" \
           "); "

    available_seat = "CREATE TABLE IF NOT EXISTS available_seat (" \
                     "seat_id text," \
                     "arena_id text," \
                     "PRIMARY KEY(seat_id, arena_id)" \
                     "); "

    reservation = "CREATE TABLE IF NOT EXISTS reservation (" \
                  "reservation_id text," \
                  "arena_id text," \
                  "seat_id text," \
                  "game_id text," \
                  "user_id text," \
                  "game_date date," \
                  "PRIMARY KEY(reservation_id)" \
                  "); "

    game = "CREATE TABLE IF NOT EXISTS game (" \
           "game_id text," \
           "team_1 text," \
           "team_2 text," \
           "arena_id int," \
           "game_date date," \
           "PRIMARY KEY(game_id)" \
           "); "

    user = "CREATE TABLE IF NOT EXISTS user (" \
           "user_id text," \
           "mail text," \
           "username text," \
           "PRIMARY KEY (user_id)" \
           "); "

    tables = [arena, seat, available_seat, reservation, game, user]

    @staticmethod
    def cleanup() -> List[str]:
        queries = ["DROP TABLE IF EXISTS arena; ",
                   "DROP TABLE IF EXISTS seat; ",
                   "DROP TABLE IF EXISTS available_seat; ",
                   "DROP TABLE IF EXISTS reservation; ",
                   "DROP TABLE IF EXISTS game; ",
                   "DROP TABLE IF EXISTS user; "]

        return queries
