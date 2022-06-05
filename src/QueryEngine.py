from typing import Any, List
from uuid import UUID


class QueryEngine:
    """
    Would you like some tea, stranger?
    """

    @staticmethod
    def _map_to_str(column_type, value):
        if column_type == 'text' or column_type == 'date':
            return f"'{value}'"
        else:
            return f"{value}"

    def update_record(self, table_name: str, column: str, column_type: str, value: Any, where_column: str,
                      where_value: Any, *args) -> str:
        query = f"UPDATE {table_name} SET {column} = {self._map_to_str(column_type, value)} " \
                f"WHERE {where_column} = {self._map_to_str(column_type, where_value)} IF EXISTS;"
        return query

    def query_record(self, table_name: str, columns: str, where_column: List[str], column_type: List[str], where_value: List[Any],
                     *args) -> str:
        parts = []
        for col, t, val in zip(where_column, column_type, where_value):
            part = f"{col} = {self._map_to_str(t, val)}"
            parts.append(part)

        where = ' AND '.join(parts)
        where = 'WHERE ' + where
        query = f"SELECT {columns} from {table_name} {where};"
        return query

    @staticmethod
    def query_all_records(table_name: str, columns: str) -> str:
        query = f"SELECT {columns} FROM {table_name} ;"
        return query

    @staticmethod
    def delete_record(table_name: str, where_column: str, where_value: UUID, *args) -> str:
        query = f"DELETE FROM {table_name} WHERE {where_column} = '{where_value}' IF EXISTS;"
        return query

    def insert_record(self, table_name: str, columns: List[str], columns_types: List[str], values: List[Any],
                      *args) -> str:

        columns_str = ""
        values_str = ""
        for column, column_type, value in zip(columns, columns_types, values):
            columns_str += column
            columns_str += ", "
            values_str += self._map_to_str(column_type, value)
            values_str += ", "

        values_str = values_str[:-2]
        columns_str = columns_str[:-2]

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
        return query
