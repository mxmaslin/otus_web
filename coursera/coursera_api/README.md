# Educational site

The task is to implement sending emails asynchronously.

Prior to exploring the project, install the requirements:

    pip install -r requirements.txt
    
To make things work, 

1. Start redis: `redis-server`
2. Start celery: `celery worker -A coursera_api --loglevel=debug --concurrency=4`
3. Start django: `./manage.py runserver`
4. Send email using form at `127.0.0.1:8000/feedback/`

The file based email backend is used in current project,
so the emails are stored in project's `tmp/feedback` folder.
    
The application developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.