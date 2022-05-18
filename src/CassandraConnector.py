from cassandra.cluster import Cluster
from db.entity import Entity


class CassandraConnector:

    def __init__(self, ip_address, port, keyspace):
        self.cluster = Cluster([ip_address], port)
        self.session = None
        self._create_session(keyspace)
        self._create_tables()

    def _create_session(self, keyspace: str, replication_factor: int = 3, strategy: str = 'SimpleStrategy') -> None:
        """
        Initialize cassandra session and create keyspace
        :param keyspace: a string with the desired keyspace name
        """
        self.session = self.cluster.connect()
        command = f"CREATE KEYSPACE IF NOT EXISTS {keyspace}  WITH REPLICATION = " + \
                  "{" + f"'class': {strategy},'replication_factor': {replication_factor}" \
                  + "};"

        self.session.execute(command)
        self.session.set_keyspace(keyspace)

    def _create_tables(self) -> None:
        """
        Initialize tables according to the schemas available in db.Entity
        """
        for table in Entity.tables:
            self.session.execute(table)
