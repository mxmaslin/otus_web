import os, sys
import pytest
sys.path.insert(0, os.path.abspath('..'))
from lotto.card_generator import shuffle_card_row
from lotto.game import Card


@pytest.fixture
def first_row_with_one():
    return [1, None, 20, None, 30, None, 40, None, 50]


@pytest.fixture
def similar_row():
    return [1, None, 20, None, 30, None, 40, None, 50]


def test_shuffle(first_row_with_one):
    shuffled = shuffle_card_row(first_row_with_one)
    assert first_row_with_one != shuffled
    sorted_initial = sorted(first_row_with_one, key=lambda x: (x is None, x))
    sorted_shuffled = sorted(shuffled, key=lambda x: (x is None, x))
    assert sorted_initial == sorted_shuffled

