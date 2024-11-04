from django.utils import timezone

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email клиента')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя', help_text='Введите полное имя')
    comment = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий', **NULLABLE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_clients',
        verbose_name="Автор",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Заголовок сообщения', help_text='Введите заголовок')
    body = models.TextField(verbose_name='Содержание сообщения', help_text='Введите текст сообщения')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_message',
        verbose_name="Автор",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    PERIOD_CHOICES = [
        ('once', 'Однократная'),
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная')
    ]

    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиенты')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.SET_NULL,
                                **NULLABLE)
    start_datetime = models.DateTimeField(default=timezone.now, verbose_name='Дата и время отправки рассылки')
    periodicity = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='once', verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name='Активность рассылки')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_mailings',
        verbose_name="Автор",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("-start_datetime",)

    def __str__(self):
        return (f"Рассылка сообщения '{self.message}' с периодичностью '{self.get_periodicity_display()}'"
            f" и статусом '{self.get_status_display()}', автор: {self.author}")


class MailingAttempt(models.Model):
    STATUSES = [("success", "успешно"), ("failed", "не успешно")]
    mailing = models.ForeignKey(Mailing, related_name='attempts', on_delete=models.CASCADE,
                                verbose_name="Попытка рассылки")
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки", editable=False)
    status = models.CharField(choices=STATUSES, verbose_name="Статус отправки")
    server_response = models.TextField(**NULLABLE, verbose_name="Ответ почтового сервера")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("-last_attempt", "status")

    def __str__(self):
        return (f"Попытка рассылки: {self.mailing}, дата и время рассылки: {self.last_attempt}, "
                f"статус: {self.get_status_display()}")
