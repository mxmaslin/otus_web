import os, sys
import pytest
sys.path.insert(0, os.path.abspath('..'))
from lotto.card_generator import (
    generate_card, generate_cards, shuffle_card_row, give_card
)
from lotto.game import Card


max_num_players = 6


@pytest.fixture
def first_row_with_one():
    return [1, None, 20, None, 30, None, 40, None, 50]


@pytest.fixture
def similar_row():
    return [1, None, 20, None, 30, None, 40, None, 50]


@pytest.fixture
def cards():
    return generate_cards(max_num_players)


@pytest.fixture
def card():
    return generate_card()


def test_shuffled_not_same(first_row_with_one):
    shuffled = shuffle_card_row(first_row_with_one)
    assert first_row_with_one != shuffled


def test_shuffled_same_digits(first_row_with_one):
    shuffled = shuffle_card_row(first_row_with_one)
    sorted_initial = sorted(first_row_with_one, key=lambda x: (x is None, x))
    sorted_shuffled = sorted(shuffled, key=lambda x: (x is None, x))
    assert sorted_initial == sorted_shuffled


def test_generated_cards_len(cards):
    assert len(cards) == max_num_players


def test_all_cards_are_cards(cards):
    assert all([isinstance(x, Card) for x in cards])


def test_card_fields_are_present(card):
    assert all([
        hasattr(card, 'first_row'),
        hasattr(card, 'second_row'),
        hasattr(card, 'last_row'),
    ]) == True


def test_card_fields_length(card):
    assert all([
        len(card.first_row) == 9,
        len(card.second_row) == 9,
        len(card.last_row) == 9,
    ]) == True


def test_card_has_five_digits(card):
    for _ in (card.first_row, card.second_row, card.last_row):
        has_five_digits = len(
            [x for x in card.first_row if isinstance(x, int)]) == 5
        if not has_five_digits:
            break
    assert has_five_digits == True


def test_card_first_digit(cards):
    fair_card_digit = True
    for _ in range(max_num_players):
        card = give_card(cards)
        for row in (card.first_row, card.second_row, card.last_row):
            fair_card_digit = row[0] is None or row[0] < 10
            if not fair_card_digit:
                break
    assert fair_card_digit == True



'''
Класс Card
- проверка совпадения двух карт
- проверка обновления карты
- проверка завершённости карты
Класс Sack
- размер 90 бочонков
Класс Host
- ask_player ?
Класс Game
- get_num_players ?
- generate_player ?
'''
