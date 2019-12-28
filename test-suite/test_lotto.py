import os, sys
import pytest
import mock
import builtins
sys.path.insert(0, os.path.abspath('..'))
from lotto.card_generator import (
    generate_card, generate_cards, shuffle_card_row, give_card
)
from lotto.game import Card, Game, Player, Sack


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
def random_card():
    return generate_card()


@pytest.fixture
def card():
    first_row = [1, None, 20, None, 30, None, 40, None, 50, None]
    second_row = [None, 21, None, 22, None, 23, None, 24, 25]
    last_row = [26, None, 27, None, 28, None, 29, None, 30]
    return Card(first_row, second_row, last_row)


@pytest.fixture
def similar_card():
    first_row = [1, None, 20, None, 30, None, 40, None, 50, None]
    second_row = [None, 21, None, 22, None, 23, None, 24, 25]
    last_row = [26, None, 27, None, 28, None, 29, None, 30]
    return Card(first_row, second_row, last_row)


@pytest.fixture
def completed_card():
    first_row = [None, None, None, None, None, None, None, None, None, None]
    second_row = first_row[:]
    last_row = second_row[:]
    return Card(first_row, second_row, last_row)


@pytest.fixture
def sack():
    return Sack()


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


def test_card_fields_are_present(random_card):
    assert all([
        hasattr(random_card, 'first_row'),
        hasattr(random_card, 'second_row'),
        hasattr(random_card, 'last_row'),
    ]) == True


def test_card_fields_length(random_card):
    assert all([
        len(random_card.first_row) == 9,
        len(random_card.second_row) == 9,
        len(random_card.last_row) == 9,
    ]) == True


def test_card_has_five_digits(random_card):
    for _ in (random_card.first_row, random_card.second_row, random_card.last_row):
        has_five_digits = len(
            [x for x in random_card.first_row if isinstance(x, int)]) == 5
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


def test_same_cards(card, similar_card):
    assert card == similar_card


def test_check_completed_card(completed_card):
    assert completed_card.is_complete == True


def test_check_not_completed_card(card):
    assert card.is_complete == False


def test_sack_size(sack):
    assert len(sack.barrels) == 90


def test_get_num_players():
    with mock.patch.object(builtins, 'input', lambda _: "5"):
        assert Game.get_num_players() == 5


def test_generate_player_return(card):
    num_players = 2
    with mock.patch.object(builtins, 'input', lambda _: (num_players, "Maxim")):
        assert isinstance(Game.generate_player(num_players, card), Player) == True
