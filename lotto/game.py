import random
from itertools import chain


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


class CardGenerator:
    _cards = []

    @staticmethod
    def _get_use_digit_in_first_column(probability=2/3):
        return random.random() < probability

    @staticmethod
    def _generate_row_digits(
            previous_rows, first_digit=None, last_card=False
    ):
        end_of_range = 90 if last_card else 89
        digits = [first_digit] if first_digit else []
        previous_rows = previous_rows or []
        amount_of_digits_in_row = 5
        while len(digits) < amount_of_digits_in_row:
            digit = random.randint(10, end_of_range)
            if digit not in digits and digit not in previous_rows:
                digits.append(digit)
        return digits

    @classmethod
    def _generate_row(cls, previous_rows, last=False):
        row = []
        use_digit_in_first_column = cls._get_use_digit_in_first_column()
        if use_digit_in_first_column:
            first_digit = random.randint(1, 9)
            row_digits = cls._generate_row_digits(
                previous_rows,
                first_digit=first_digit,
                last_card=last
            )
            row.extend(row_digits)
        else:
            row.extend(cls._generate_row_digits(previous_rows, last_card=last))
        row = sorted(row)
        nones = [None] * 4
        row.extend(nones)
        return row

    @classmethod
    def _generate_card(cls):
        first_row = cls._generate_row(None)
        second_row = cls._generate_row(first_row)
        previous_rows = first_row + second_row
        last_row = cls._generate_row(previous_rows, last=True)
        return Card(first_row, second_row, last_row)

    @classmethod
    def generate_cards(cls, num_players):
        while len(cls._cards) < num_players:
            card = cls._generate_card()
            if card not in cls._cards:
                cls._cards.append(card)
        return cls._cards

    @staticmethod
    def _shuffle_card_row(row):
        if row[0] < 10:
            return [row[0]] + random.sample(row[1:], len(row) - 1)
        row.remove(None)
        return [None] + random.sample(row, len(row))

    @classmethod
    def give_card(cls):
        try:
            card = cls._cards.pop()
        except IndexError:
            return None
        else:
            card.first_row = cls._shuffle_card_row(card.first_row)
            card.second_row = cls._shuffle_card_row(card.second_row)
            card.last_row = cls._shuffle_card_row(card.last_row)
            return card


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
    def __init__(self, sack, generator, num_cards=24):
        super().__init__()
        self.sack = sack
        self.generator = generator
        self.generator.generate_cards(num_cards)

    def pick_barrel(self):
        try:
            return self.sack.barrels.pop()
        except IndexError:
            print('В мешочке больше нет бочонков')

    def give_card(self):
        return self.generator.give_card()

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
    card_generator = CardGenerator()
    host = Host(sack, card_generator, num_players)
    players = [
        game.generate_player(i, host.give_card()) for i in range(1, num_players + 1)
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
