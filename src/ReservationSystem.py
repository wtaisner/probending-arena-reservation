import uuid
import time
from typing import Dict

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
            result = pyip.inputMenu(
                ['list games', 'reservation', 'quit'], lettered=True)
            if result == 'finish':
                break
            elif result == 'reservation':
                self._reservation_parser()
                break
                # TODO: implement reservation process
            elif result == 'list games':
                self._list_all_games()
            print('=========================================================')

    def _get_arena_name_by_id(self, arena_id: str) -> str:
        """
        utility function to get arena name by id
        :param arena_id: string with arena_id
        :return: arena name
        """
        arena_name_query = self.query_engine.query_record(
            'arena', 'name', ['arena_id'], ['UUID'], [arena_id])
        arena_name = self.client.execute_query(arena_name_query)[0][0]
        return arena_name

    def _list_all_games(self) -> None:
        """
        simple utility function to print all available games
        """
        query = self.query_engine.query_all_records(
            'game', 'arena_id, team_1, team_2, game_date')
        result_set = self.client.execute_query(query)
        for res in result_set:
            arena_id, team_1, team_2, game_date = res
            arena_name = self._get_arena_name_by_id(arena_id)
            print(f'- {team_1} vs {team_2} at {arena_name} on {game_date}\n')

    def _get_all_games(self) -> Dict[str, str]:
        """
        get all games in dictionary, in which a string describing the game is the key, and game_id is the value
        # TODO: consider changing key to be a smaller cancer
        :return: dictionary as above
        """
        query = self.query_engine.query_all_records(
            'game', 'game_id, arena_id, team_1, team_2, game_date', )
        result_set = self.client.execute_query(query)
        games = dict()
        for res in result_set:
            game_id, arena_id, team_1, team_2, game_date = res
            arena_name = self._get_arena_name_by_id(arena_id)
            games[f'- {team_1} vs {team_2} at {arena_name} on {game_date}'] = game_id
        return games

    def _reservation_parser(self) -> str:
        """
        utility function; displays menu choice for user, returns corresponding game_id
        :return: string with game_id
        """
        games = self._get_all_games()
        names = list(games.keys())
        result = pyip.inputMenu(names, lettered=True)

        game_id = games[result]
        query = self.query_engine.query_record(
            'game', 'available_seats', ['game_id'], ['UUID'], [game_id])
        result_set = self.client.execute_query(query)[0][0]

        if len(result_set) > 0:
            seats = [str(i) for i in result_set]

            # TODO: no available seats @annprzy
            seat = int(pyip.inputMenu(seats))

            result_set.remove(seat)

            query = self.query_engine.update_record(
                'game', 'available_seats', 'list', result_set, 'game_id', game_id)
            self.client.execute_query(query)

            user_name = pyip.inputStr('Name:')
            # TODO: mail validation @wtaisner
            user_email = pyip.inputStr('Email:')
            reservation_id = uuid.uuid4()

            data = [reservation_id, seat, game_id, user_name, user_email]
            columns = ['reservation_id', 'seat_id',
                       'game_id', 'user', 'user_email']
            columns_types = ['UUID', 'int', 'UUID', 'text', 'text']
            query = self.query_engine.insert_record(
                'reservation', columns, columns_types, data)
            self.client.execute_query(query)

            time.sleep(1)
            query = self.query_engine.query_record(
                'reservation', 'reservation_id', ['game_id', 'seat_id'], ['UUID', 'int'], [game_id, seat])
            result_set = self.client.execute_query(query)[0][0]

            if result_set == reservation_id:
                print('Seat reserved - if noone tried to reserve it after you :)')
            else:
                print('We were not able to fulfill your request')

        else:
            print("All seats taken")

        return games[result]
