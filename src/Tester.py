import multiprocessing
import random
import time
from multiprocessing import Pool
from typing import Tuple

import uuid
from src.CassandraConnector import *
from src.QueryEngine import QueryEngine


def _random_action_1(client: CassandraConnector) -> None:
    query_engine = QueryEngine()
    print('1')


def _random_action_2(client: CassandraConnector) -> None:
    query_engine = QueryEngine()
    print('2')


def _random_action_3(client: CassandraConnector) -> None:
    query_engine = QueryEngine()
    print('3')


def _perform_random_action(num: int):
    client = connect(initialize=False)
    for _ in range(num):
        available_actions = [_random_action_1, _random_action_2, _random_action_3]
        execute = random.choice(available_actions)
        print(f"Current user {multiprocessing.current_process().pid}; action: ")
        execute(client=client)


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
        print(f'Current user: {user_name} Result should be equal to None (or something similar); result = {res.all()}')

        res_query = query_engine.query_all_records('reservation', 'user')
        result = client.execute_query(res_query)
        for res in result:
            print(res)
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
    with Pool(2) as p:
        p.map(_perform_random_action, [1000, 1000])


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
