from django.core.management import BaseCommand

from mailing.tasks import send_mailings


class Command(BaseCommand):
    help = "Запуск рассылок вручную"

    def handle(self, *args, **options):
        print("Запуск отправки рассылок...")
        send_mailings()
        print("Отправка рассылок завершена.")
