from cassandra.cluster import Cluster


class CassandraConnector:

    def __init__(self, ip_address, port, keyspace):
        self.cluster = Cluster([ip_address], port)
        self.session = None
        self._create_session(keyspace)

    def _create_session(self, keyspace):
        self.session = self.cluster.connect()
        command = f"CREATE KEYSPACE IF NOT EXISTS {keyspace} " + " WITH REPLICATION = {'class': 'SimpleStrategy','replication_factor': 3};"
        self.session.execute(command)
        self.session.set_keyspace(keyspace)

