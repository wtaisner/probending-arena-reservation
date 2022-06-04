import time
from src.CassandraConnector import CassandraConnector
from src.QueryEngine import QueryEngine


class Tester:
    def __init__(self, client: CassandraConnector) -> None:
        self.client = client
        self.query_engine = QueryEngine()

    def stress_test_1(self):
        """
        A client performs the same query "very fast"
        :return:
        """
        print('Stress test 1: a client performs the same query very fast')
        repeats = 1000
        print(f'number of executions: {repeats}')
        print('=========================================================')

        start_time = time.time()
        for i in range(repeats):
            query = self.query_engine.query_all_records('game', '*')
            result_set = self.client.execute_query(query)
        end_time = time.time() - start_time
        print(f'Total time: {end_time:.4f} s')

    def stress_test_2(self):
        """
        Two or more users perform possible actions randomly
        :return:
        """
        pass

    def stress_test_3(self):
        """
        Instant reservation of all available seats
        :return:
        """
        pass
