class Entity:

    arena = "CREATE TABLE IF NOT EXISTS arena (" \
            "arena_id int," \
            "name text," \
            "addres text," \
            "PRIMARY KEY(arena_id)" \
            "); "

    seat = "CREATE TABLE IF NOT EXISTS seat (" \
           "seat_id int," \
           "arena_id int," \
           "PRIMARY KEY(seat_id)" \
           "); "

    reservation = "CREATE TABLE IF NOT EXISTS reservation (" \
                  "reservation_id int," \
                  "arena_id int," \
                  "seat_id int," \
                  "game_id int," \
                  "user_id int," \
                  "game_date date," \
                  "PRIMARY KEY(reservation_id)" \
                  "); "

    game = "CREATE TABLE IF NOT EXISTS game (" \
           "game_id int," \
           "team_1 text," \
           "team_2 text," \
           "arena_id int," \
           "game_date date," \
           "PRIMARY KEY(game_id)" \
           "); "

    user = "CREATE TABLE IF NOT EXISTS user (" \
           "user_id int," \
           "mail text," \
           "username text," \
           "PRIMARY KEY (user_id)" \
           "); "

    tables = [arena, seat, reservation, game, user]
