# Test suite

Test suite for [google search fetcher](https://github.com/mxmaslin/otus_web/tree/master/google-search-fetcher) and [russian lotto](https://github.com/mxmaslin/otus_web/tree/master/lotto) projects.  

Prior to start, install the requirements:

```bash
pip install -r requirements.txt
```

Run all the tests:

```bash
pytest
```

Run tests for fetcher:

```bash
pytest -q -s --query 'сколько сейчас времени' --amount 10 recursive 0

pytest -q -s --query где 'ближайший макдональдс' --amount 5 recursive 1
```

Run tests for lotto:

```bash
pytest test_lotto.py
```


The program developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.