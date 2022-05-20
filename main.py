from src.CassandraConnector import CassandraConnector
from src.QueryEngine import QueryEngine


def main() -> None:

    client = CassandraConnector("172.17.0.2", 9042, 'atla')

    query = QueryEngine()

    res = client.session.execute("SELECT * FROM arena")
    print(res.one())
    res = client.session.execute("SELECT * FROM seat")
    print(res.one())


if __name__ == '__main__':
    main()
