from django.core import mail

from coursera_queue.celery import app


@app.task
def send_email_task(data):
    recipient = data['recipient']
    subject = data['subject']
    message = data['message']
    sender = data['sender']
    cc_myself = data['cc_myself']
    recipients = [recipient, sender] if cc_myself else [recipient]
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject, message, sender, recipients, connection=connection,
        ).send()


