import time
import uuid

from src.CassandraConnector import CassandraConnector
from src.QueryEngine import QueryEngine


class Tester:
    def __init__(self, client: CassandraConnector) -> None:
        self.client = client
        self.query_engine = QueryEngine()

    def stress_test_1(self) -> None:
        """
        A client performs the same query "very fast"
        """
        print('=========================================================')
        print('Stress test 1: a client performs the same query very fast')
        repeats = 1000
        print(f'number of executions: {repeats}')
        print('=========================================================')

        start_time = time.time()
        for i in range(repeats):
            query = self.query_engine.query_all_records('game', '*')
            _ = self.client.execute_query(query)
        end_time = time.time() - start_time
        print(f'Total time: {end_time:.4f} s')

    def stress_test_2(self) -> None:
        """
        Two or more users perform possible actions randomly
        """
        pass

    def stress_test_3(self) -> None:
        """
        Instant reservation of all available seats
        """
        print('=========================================================')
        print("Stress test 3: instant reservation of all available seats")
        games = self.query_engine.query_all_records('game', '*')
        games = self.client.execute_query(games)
        print(f"Game {games[0]}")
        game_id = games[0][0]
        query = self.query_engine.query_record(
            'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
        result_set = self.client.execute_query(query)[0][0]

        if len(result_set) > 0:
            seats = [str(i) for i in result_set]
            print(f'Available seats: {seats}')
            query = 'BEGIN BATCH '
            for seat in seats:
                result_set.remove(int(seat))

                update_query = self.query_engine.update_record(
                    'game', 'available_seats', 'list', result_set, 'game_id', game_id)
                self.client.execute_query(update_query)

                user_name = "TEST_USER"
                user_email = "TEST@EMAIL.COM"
                reservation_id = uuid.uuid4()

                data = [reservation_id, seat, game_id, user_name, user_email]
                columns = ['reservation_id', 'seat_id',
                           'game_id', 'user', 'user_email']
                columns_types = ['UUID', 'int', 'UUID', 'text', 'text']
                query += self.query_engine.insert_record(
                    'reservation', columns, columns_types, data)

            query += " APPLY BATCH; "
            self.client.execute_query(query)
            print('All seats reserved')
            res_query = self.query_engine.query_record(
                'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
            res = self.client.execute_query(res_query)
            print(f'Result should be equal to None (or something similar); result = {res.all()}')
        else:
            print("All seats taken")
