def pytest_addoption(parser):
    parser.addoption("--query")
    parser.addoption("--amount")
    parser.addoption("--recursive")