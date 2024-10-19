from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore

from mailing.tasks import send_mailings


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        send_mailings,
        trigger=IntervalTrigger(minutes=1),
        id='send_mailings',
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()
    