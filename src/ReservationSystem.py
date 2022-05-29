from typing import Literal

from src.CassandraConnector import CassandraConnector
import pyinputplus as pyip

from src.QueryEngine import QueryEngine


class ReservationSystem:
    def __init__(self, client: CassandraConnector = None):
        self.client = client
        self.query_engine = QueryEngine()

    def main(self) -> None:
        print(f"**Welcome to the probending arena reservation system!**\n"
              f"This wonderful piece of software allows you to reserve a seat for your favourite bending game!\n"
              f"To select an option, simply type a number or a letter corresponding to it")
        while True:
            print("What is it that you want to do?")
            result = pyip.inputMenu(['list games', 'reservation', 'quit'], lettered=True)
            if result == 'finish':
                break
            elif result == 'reservation':
                break
                # TODO: implement reservation process
            elif result == 'list games':
                self._list_all_games()
            print('=========================================================')

    def _list_all_games(self) -> None:
        query = self.query_engine.query_all_records('game', 'arena_id, team_1, team_2, game_date')
        result_set = self.client.execute_query(query)
        for res in result_set:
            arena_id, team_1, team_2, game_date = res
            arena_name_query = self.query_engine.query_record('arena', 'name', 'arena_id', 'UUID', arena_id)
            arena_name = self.client.execute_query(arena_name_query)[0][0]
            print(f'- {team_1} vs {team_2} at {arena_name} on {game_date}')

    def _reservation_menu_parser(self):
        pass

    def _reservation_parser(self):
        pass
