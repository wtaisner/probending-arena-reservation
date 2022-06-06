import multiprocessing
import random
import time
from multiprocessing import Pool
from typing import Tuple

import uuid
from src.CassandraConnector import *
from src.QueryEngine import QueryEngine

_TABLES = ['arena', 'reservation', 'game']
_ID = ['arena_id', 'reservation_id', 'game_id']
_DATA = zip(_TABLES, _ID)


def _random_reservation(client: CassandraConnector):
    log_user = multiprocessing.current_process().pid
    query_engine = QueryEngine()
    games = query_engine.query_all_records('game', '*')
    games = client.execute_query(games)

    game = random.choice(games.all())
    game_id = game[0]
    query = query_engine.query_record(
        'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
    result_set = client.execute_query(query)[0][0]
    if result_set is None:
        print(f'{[log_user]} no games with available seats')
    elif len(result_set) > 0:
        seats = [str(i) for i in result_set]

        seat = int(random.choice(seats))
        print(f"{[log_user]} is trying to reserve seat {seat} for {game_id}")
        result_set.remove(seat)

        query = query_engine.update_record(
            'game', 'available_seats', 'list', result_set, 'game_id', game_id)
        client.execute_query(query)

        user_name = multiprocessing.current_process().pid
        user_email = multiprocessing.current_process().pid
        reservation_id = uuid.uuid4()

        data = [reservation_id, seat, game_id, user_name, user_email]
        columns = ['reservation_id', 'seat_id',
                   'game_id', 'user', 'user_email']
        columns_types = ['UUID', 'int', 'UUID', 'text', 'text']
        query = query_engine.insert_record(
            'reservation', columns, columns_types, data)
        client.execute_query(query)

        time.sleep(1)
        query = query_engine.query_record(
            'reservation', 'reservation_id', ['game_id', 'seat_id'], ['UUID', 'int'], [game_id, seat])
        result_set = client.execute_query(query)[0][0]

        if result_set == reservation_id:
            print(f'{[log_user]} Seat {seat} reserved for {game_id}')
        else:
            print(
                f'{[log_user]} We were not able to fulfill your request; seat {seat}, game_id {game_id}')

    else:
        print(f"{[log_user]} All seats taken")


def _perform_random_action(num: int):
    client = connect(initialize=False)
    for _ in range(num):
        _random_reservation(client)


def _util(data: Tuple[str, str]) -> None:
    """
    a utility function that performs a reservation of all seats on behalf of one client
    :param data - a tuple of strings containing mock username and email
    """
    user_name, user_email = data
    query_engine = QueryEngine()
    client = connect(initialize=False)

    games = query_engine.query_all_records('game', '*')
    games = client.execute_query(games)
    print(f"Game {games[0]}")
    game_id = games[0][0]
    query = query_engine.query_record(
        'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
    result_set = client.execute_query(query)[0][0]

    if result_set is not None:
        if len(result_set) > 0:
            seats = [str(i) for i in result_set]
            print(f'Current user: {user_name} Available seats: {seats}')
            query = 'BEGIN BATCH '
            for seat in seats:
                result_set.remove(int(seat))

                update_query = query_engine.update_record(
                    'game', 'available_seats', 'list', result_set, 'game_id', game_id)
                client.execute_query(update_query)

                reservation_id = uuid.uuid4()

                data = [reservation_id, seat, game_id, user_name, user_email]
                columns = ['reservation_id', 'seat_id',
                           'game_id', 'user', 'user_email']
                columns_types = ['UUID', 'int', 'UUID', 'text', 'text']
                query += query_engine.insert_record(
                    'reservation', columns, columns_types, data)

            query += " APPLY BATCH; "
            client.execute_query(query)
            print(f'Current user: {user_name} All seats reserved')
            res_query = query_engine.query_record(
                'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
            res = client.execute_query(res_query)
            print(
                f'Current user: {user_name} Result should be equal to None (or something similar); result = {res.all()}')

            res_query = query_engine.query_all_records('reservation', 'user')
            result = client.execute_query(res_query)
            for res in result:
                print(res)
            else:
                print(f"Current user: {user_name} All seats taken")
    else:
        print(f"Current user: {user_name} All seats taken")


def stress_test_1(query_engine=QueryEngine()) -> None:
    """
    A client performs the same query "very fast"
    """
    client = connect()
    print('=========================================================')
    print('Stress test 1: a client performs the same query very fast')
    repeats = 1000
    print(f'number of executions: {repeats}')
    print('=========================================================')

    start_time = time.time()
    for i in range(repeats):
        query = query_engine.query_all_records('game', '*')
        _ = client.execute_query(query)
    end_time = time.time() - start_time
    print(f'Total time: {end_time:.4f} s')


def stress_test_2() -> None:
    """
    Two or more users perform possible actions randomly
    """
    print('=========================================================')
    print('Stress test 2: two or more users perform possible actions randomly')
    user = 5
    number = 20
    print(
        f'Number of users: {user}, number of random actions of each user: {number}')
    print('=========================================================')

    with Pool(user) as p:
        p.map(_perform_random_action, [number for _ in range(user)])


def stress_test_3() -> None:
    """
    Instant reservation of all available seats
    """
    print('=========================================================')
    print("Stress test 3: instant reservation of all available seats")
    names = ['TEST_1', 'TEST_2']
    emails = ['EMAIL@ADAM.COM', 'EMAIL@GRZNDA.COM']

    with Pool(2) as p:
        p.map(_util, zip(names, emails))
