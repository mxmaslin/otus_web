import os, sys
import pytest
sys.path.insert(0, os.path.abspath('..'))
from lotto import card_generator
from lotto.game import Card
# import lotto
# from . import lotto

user_paths = sys.path
print(user_paths)


# @pytest.fixture
# def card_generator():
#     return game.CardGenerator()
#
#
# def test_generate_row_digits_first_row_first_digit(card_generator):
#     first_row_first_digit = card_generator._generate_row_digits(
#         first_digit=1
#     )
#     assert first_row_first_digit[0] == 1
#
#
# def test_generate_row_digits_first_row_no_first_digit():
#     pass
#
#
#
