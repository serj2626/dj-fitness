from fitness_project.celery import app
from .service import send_email_for_feedback, send_email_for_newsletter
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


@app.task
def send_feedback(email, name):
    send_email_for_feedback(email, name)
    return 'send_feedback is done'


@app.task
def send_newsletter(email):
    send_email_for_newsletter(email)
    return 'send_newsletter is done'


@app.task
def send_beat_email():
    for user in User.objects.all():
        send_mail(
            'Сообщение с сайта dj-fitness',
            f'Я тебя заебу со своими письмами {user.email}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    return f'Все письма дошли до адресатов'
