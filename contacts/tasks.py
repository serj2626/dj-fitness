from fitness_project.celery import app
from .service import send_email_for_feedback, send_email_for_newsletter


@app.task
def send_feedback(email, name):
    send_email_for_feedback(email, name)
    return 'send_feedback is done'


@app.task
def send_newsletter(email):
    send_email_for_newsletter(email)
    return 'send_newsletter is done'