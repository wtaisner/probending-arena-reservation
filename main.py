import pyinputplus as pyip

from src.CassandraConnector import CassandraConnector
from src.QueryEngine import QueryEngine


def connect() -> CassandraConnector:
    """
    utility function that return CassandraConnector object, which contains a session connected to Cassandra cluster
    :return: connected cassandra session
    """
    return CassandraConnector("172.17.0.2", 9042, 'atla')


def main() -> None:
    client = connect()
    while True:
        result = pyip.inputStr('Please insert your query: ')
        if result == 'grzenda-menda':
            break
        else:
            try:
                res = client.session.execute(result)
                print(res.all())
            except ValueError:
                raise ValueError('Invalid query you idiot')


if __name__ == '__main__':
    main()
