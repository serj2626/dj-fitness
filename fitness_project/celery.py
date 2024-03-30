import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_project.settings')

app = Celery('fitness_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {

    #  Название задачи
    'send-mail-every-5-minute': {

        #  Путь до задачи с рассылкой писем
        'task': 'contacts.tasks.send_beat_email',

        #  Расписание с помощью модуля crontab
        'schedule': crontab(minute='*/2'),

        #  Аргументы для функции в модуле tasks.py
        # 'args': (16, 16),
    },
}
