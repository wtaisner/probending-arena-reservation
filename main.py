from src.CassandraConnector import connect
from src.ReservationSystem import ReservationSystem


def main() -> None:
    client = connect()
    rs = ReservationSystem(client)
    rs.main()


if __name__ == '__main__':
    main()
