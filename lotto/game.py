import random
from itertools import chain

from card_generator import generate_cards, give_card


class NumPlayersException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class Card:
    def __init__(self, first_row, second_row, last_row):
        self.first_row = first_row
        self.second_row = second_row
        self.last_row = last_row

    def __eq__(self, other):
        return all([
            self.first_row == other.first_row,
            self.second_row == other.second_row,
            self.last_row == other.last_row
        ])

    def update(self, barrel):
        for row in (self.first_row, self.second_row, self.last_row):
            for i in range(len(row)):
                row[i] = None if row[i] == barrel.digit else row[i]

    def __iter__(self):
        return (x for x in chain(self.first_row, self.second_row, self.last_row))

    @property
    def is_complete(self):
        return any([
            all(self.first_row), all(self.second_row), all(self.last_row)
        ])

    def __str__(self):
        return '\n'.join([
            ' '.join(str(x) if x else 'X' for x in row)
            for row in (self.first_row, self.second_row, self.last_row)
        ])


class Player:
    def __init__(self, name, card):
        self.name = name
        self.card = card

    def __str__(self):
        return f'Игрок {self.name}'


class Barrel:
    def __init__(self, digit):
        self.digit = digit

    def __str__(self):
        return f'Бочонок с цифрой {self.digit}'


class Sack:
    num_barrels = 90

    def __init__(self):
        super().__init__()
        self.barrels = self._fill_with_barrels()

    def _fill_with_barrels(self):
        barrels = [Barrel(i) for i in range(1, self.num_barrels + 1)]
        random.shuffle(barrels)
        return barrels

    def __iter__(self):
        return (x for x in self.barrels)

    def __str__(self):
        barrels_digits = ' '.join(
            map(str, [barrel.digit for barrel in self.barrels])
        )
        return f'Содержимое мешочка: {barrels_digits}'


class Host:
    def __init__(self, sack, num_cards=24):
        super().__init__()
        self.sack = sack

    def pick_barrel(self):
        try:
            return self.sack.barrels.pop()
        except IndexError:
            print('В мешочке больше нет бочонков')

    @staticmethod
    def check_card(player, barrel):
        return barrel.digit in chain(
            player.card.first_row, player.card.second_row, player.card.last_row
        )

    @staticmethod
    def ask_player(player, barrel):
        while True:
            print(f'{player}, на вашей карточке есть цифра {barrel.digit}?')
            print('У вас такая карточка:')
            print(player.card)
            try:
                player_answer = input('да/нет: ').lower()
            except UnicodeDecodeError:
                print('Ошибка распознавания ввода, повторите ввод')
                continue
            if player_answer not in ['да', 'нет']:
                print('Пожалуйста, ответьте "да" или "нет"')
            else:
                return player_answer


class Game:
    @staticmethod
    def get_num_players():
        while True:
            try:
                num_players = int(
                    input('Введите количество игроков (от 2 до 6): ')
                )
                if num_players < 2 or num_players > 6:
                    raise NumPlayersException(
                        'Количество игроков должно быть от 2 до 6',
                        'Number value error'
                    )
            except (ValueError, NumPlayersException, UnicodeDecodeError) as e:
                print(e)
            else:
                return num_players

    @staticmethod
    def generate_player(i, card):
        while True:
            try:
                player_name = input(f'Введите имя игрока {i}: ')
            except UnicodeDecodeError:
                print('Ошибка распознавания ввода, повторие ввод')
            else:
                break
        return Player(player_name, card)


def main():
    game = Game()
    num_players = game.get_num_players()
    sack = Sack()
    host = Host(sack, num_players)
    cards = generate_cards(num_players)
    players = [
        game.generate_player(i, give_card(cards)) for i in range(1, num_players + 1)
    ]
    while host.sack.barrels:
        barrel = host.pick_barrel()
        for player in players[:]:
            player_answer = host.ask_player(player, barrel)
            digit_on_card = host.check_card(player, barrel)
            if player_answer == 'да':
                if digit_on_card:
                    print(f'{player}, обновляю вашу карточку')
                    player.card.update(barrel)
                    if player.card.is_complete:
                        print(f'{player} выиграл!')
                        return
                else:
                    print(f'{player} ошибся, у него нет такой цифры. Игрок выбывает из игры')
                    players.remove(player)
            else:
                if digit_on_card:
                    print(f'{player} ошибся, у него есть такая цифра. Игрок выбывает из игры')
                    players.remove(player)
            if len(players) < 2:
                print(f'{players[0]} выиграл!')
                return
            print()
    else:
        print('Ничья')


if __name__ == '__main__':
    main()
