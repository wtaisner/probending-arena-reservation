from cassandra.cluster import Cluster
from .db.table import Table
from .db.initial_entities import God

TABLE_ENTITY = Table()
GOD = God()


class CassandraConnector:

    def __init__(self, ip_address, port, keyspace):
        self.cluster = Cluster([ip_address], port)
        self.session = None
        self._create_session(keyspace)
        self._create_tables()
        self._populate()

    def _create_session(self, keyspace: str, replication_factor: int = 3, strategy: str = 'SimpleStrategy') -> None:
        """
        Initialize cassandra session and create keyspace
        :param keyspace: a string with the desired keyspace name
        """
        self.session = self.cluster.connect()
        self.session.default_timeout = 40
        command = f"CREATE KEYSPACE IF NOT EXISTS {keyspace}  WITH REPLICATION = " + \
                  "{" + f"'class': '{strategy}','replication_factor': {replication_factor}" \
                  + "};"

        self.session.execute(command)
        self.session.execute(f"USE {keyspace};")
        self.session.set_keyspace(keyspace)

    def _create_tables(self) -> None:
        """
        Initialize tables according to the schemas available in db.Entity
        """
        # drop all tables -> DROP TABLE command doesn't stack, hence list
        queries = TABLE_ENTITY.cleanup()
        for query in queries:
            self.session.execute(query)
        print("LOG: tables cleared")

        # recreate all tables
        for table in TABLE_ENTITY.tables:
            self.session.execute(table)
        print("LOG: tables created")

    def _populate(self) -> None:
        """
        Populate the tables with the initial data
        """
        for query in GOD.populate():
            self.session.execute(query)
        print("LOG: initial entities inserted")

    def execute_query(self, query: str) -> None:
        """
        execute external query
        :param query: CQL query
        :return: None
        """
        try:
            res = self.session.execute(query)
            print(res.all())
        except:
            print("Invalid query, please try again.")
