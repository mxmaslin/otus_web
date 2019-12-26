import random


def get_use_digit_in_first_column(probability=2/3):
    return random.random() < probability


def generate_row_digits(
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


def generate_row(previous_rows, last=False):
    row = []
    use_digit_in_first_column = get_use_digit_in_first_column()
    if use_digit_in_first_column:
        first_digit = random.randint(1, 9)
        row_digits = generate_row_digits(
            previous_rows,
            first_digit=first_digit,
            last_card=last
        )
        row.extend(row_digits)
    else:
        row.extend(generate_row_digits(previous_rows, last_card=last))
    row = sorted(row)
    nones = [None] * 4
    row.extend(nones)
    return row


def generate_card():
    from .game import Card
    first_row = generate_row(None)
    second_row = generate_row(first_row)
    previous_rows = first_row + second_row
    last_row = generate_row(previous_rows, last=True)
    return Card(first_row, second_row, last_row)


def generate_cards(num_players):
    cards = []
    while len(cards) < num_players:
        card = generate_card()
        if card not in cards:
            cards.append(card)
    return cards


def shuffle_card_row(row):
    if row[0] < 10:
        return [row[0]] + random.sample(row[1:], len(row) - 1)
    row.remove(None)
    return [None] + random.sample(row, len(row))


def give_card(cards):
    try:
        card = cards.pop()
    except IndexError:
        return None
    else:
        card.first_row = shuffle_card_row(card.first_row)
        card.second_row = shuffle_card_row(card.second_row)
        card.last_row = shuffle_card_row(card.last_row)
        return card
