import random
import time


class NumPlayersException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


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


class Card:
    num_digits = 15

    def __init__(self):
        self.digits = Card._generate_digits(self)

    @staticmethod
    def _generate_digits(cls):
        digits = {}
        while len(digits) < 15:
            digit = random.randint(1, 90)
            digits[digit] = False
        return digits

    def update(self, digit):
        self.digits[digit] = True

    @property
    def is_complete(self):
        return all(self.digits.values())

    def __str__(self):
        card = [
            f'({digit})' if self.digits[digit] else str(digit)
            for digit in sorted(self.digits)
        ]
        card = [' '.join(x) for x in ([card[0:5], card[5:10], card[10:15]])]
        return f'Цифры на его карточке:\n{card[0]}\n{card[1]}\n{card[2]}'


class Sack:
    num_barrels = 90

    def __init__(self):
        self.barrels = Sack._fill_with_barrels(self)

    @staticmethod
    def _fill_with_barrels(cls):
        barrels = [Barrel(i) for i in range(1, cls.num_barrels + 1)]
        random.shuffle(barrels)
        return barrels

    def pick_barrel(self):
        return self.barrels.pop(random.randrange(len(self.barrels)))

    def __iter__(self):
        return self.barrels

    def __str__(self):
        barrels_digits = ' '.join(
            map(str, [barrel.digit for barrel in self.barrels])
        )
        return f'Содержимое мешочка: {barrels_digits}'


def get_num_players():
    while True:
        try:
            num_players = int(input('Введите количество игроков (от 2 до 6): '))
            if num_players < 2 or num_players > 6:
                raise NumPlayersException(
                    'Количество игроков должно быть от 2 до 6',
                    'Number value error'
                )
        except (ValueError, NumPlayersException) as e:
            print(e)
        else:
            return num_players


def get_players(num_players):
    players = []
    for i in range(1, num_players + 1):
        player_name = input(f'Введите имя игрока {i}: ')
        player_card = Card()
        player = Player(player_name, player_card)
        players.append(player)
    return players


def main():
    num_players = get_num_players()
    players = get_players(num_players)
    sack = Sack()
    print()
    i = 0
    while sack.barrels:
        for picker in players:
            barrel = sack.pick_barrel()
            i += 1
            print(f'{picker} берет {barrel}')
            for player in players:
                if barrel.digit in player.card.digits:
                    print(f'Цифра на бочонке есть в карточке {player}')
                    player.card.update(barrel.digit)
                    print(player.card)
                    if player.card.is_complete:
                        print(f'{player} выиграл на {i} бочонке!')
                        return
            print()
            time.sleep(1)
            print()


if __name__ == '__main__':
    main()
