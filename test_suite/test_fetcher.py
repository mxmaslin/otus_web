import os, sys
import pytest
import validators
sys.path.insert(0, os.path.abspath('..'))
from fetcher.fetcher import get_search_result



@pytest.fixture()
def query(pytestconfig):
    return pytestconfig.getoption('query')


@pytest.fixture()
def amount(pytestconfig):
    return pytestconfig.getoption('amount')


@pytest.fixture()
def recursive(pytestconfig):
    return pytestconfig.getoption('recursive')


def test_time_5_0_len(query, amount, recursive):
    if query == 'сколько сейчас времени' and amount == 5 and recursive == 0:
        search_result = get_search_result(query, amount, recursive)
        assert len(search_result) == 5
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0


def test_time_5_0_recursive(query, amount, recursive):
    if query == 'сколько сейчас времени' and amount == 5 and recursive == 0:
        search_result = get_search_result(query, amount, recursive)
        fetched = [len(x['fetched']) for x in search_result]
        assert any(fetched) is False
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0


def test_time_5_0_urls(query, amount, recursive):
    if query == 'сколько сейчас времени' and amount == 5 and recursive == 0:
        search_result = get_search_result(query, amount, recursive)
        urls = [validators.url(x['url']) for x in search_result]
        assert all(urls) is True
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0


def test_mac_10_1_len(query, amount, recursive):
    if query == 'где ближайший макдонадльдс' and amount == 5 and recursive == 0:
        search_result = get_search_result(query, amount, recursive)
        assert len(search_result) == 10
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0


def test_mac_10_1_recursive(query, amount, recursive):
    if query == 'где ближайший макдонадльдс' and amount == 10 and recursive == 1:
        search_result = get_search_result(query, amount, recursive)
        fetched = [len(x['fetched']) for x in search_result]
        assert all(fetched) is True
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0


def test_mac_10_1_urls(query, amount, recursive):
    if query == 'где ближайший макдонадльдс' and amount == 10 and recursive == 1:
        search_result = get_search_result(query, amount, recursive)
        urls = [validators.url(x['url']) for x in search_result]
        assert all(urls) is True
    else:
        print('Используйте аргументы командной строки, указанные в README')
        assert 1 == 0