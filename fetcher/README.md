# Google search fetcher

The program fetches google search result urls, like so:

```bash
python fetcher.py --query question of life, the universe and everything --amount 5 --recursive 1
```

Keys:

- `--query` The query to google
- `--amount` Desired amount of url in result
- `--recursive` When this key is true, each url will be inspected, and all links on its page will be printed

Prior to use, please install requirements:

```bash
pip install -r requirements.txt
```

The application developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.
