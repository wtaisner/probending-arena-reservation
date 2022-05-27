import pyinputplus as pyip

from src.CassandraConnector import CassandraConnector
from src.ReservationSystem import ReservationSystem


def connect() -> CassandraConnector:
    """
    utility function that return CassandraConnector object, which contains a session connected to Cassandra cluster
    :return: connected cassandra session
    """
    return CassandraConnector("172.17.0.2", 9042, 'atla')


def main() -> None:
    client = connect()
    rs = ReservationSystem(client)
    rs.main()
    # while True:
    #     query = pyip.inputStr('Please insert your query: ')
    #     if query == 'finish':
    #         break
    #     else:
    #         client.execute_query(query)


if __name__ == '__main__':
    main()
