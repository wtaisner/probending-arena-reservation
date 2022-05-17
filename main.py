from src.CassandraConnector import CassandraConnector


def main():

    client = CassandraConnector("172.17.0.2", 9042, 'atla')


if __name__ == '__main__':
    main()
