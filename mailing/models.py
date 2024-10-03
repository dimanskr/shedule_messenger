from django.db import models

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email клиента', unique=True)
    full_name = models.CharField(max_length=255, verbose_name='Полное имя', help_text='Введите полное имя')
    comment = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий', **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Заголовок сообщения', help_text='Введите заголовок')
    body = models.TextField(verbose_name='Содержание сообщения', help_text='Введите текст сообщения')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная')
    ]

    client = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиент')
    message = models.ForeignKey(Message, related_name='mailings', verbose_name='Сообщение', on_delete=models.SET_NULL,
                                **NULLABLE)
    start_datetime = models.DateTimeField(verbose_name='Дата и время первой отправки рассылки')
    periodicity = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='daily')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("-start_datetime",)

        def __str__(self):
            return f"Рассылка {self.pk}"


class MailingAttempt(models.Model):
    STATUSES = [("success", "успешно"), ("success", "не успешно")]
    mailing = models.ForeignKey(Mailing, related_name='attempts', on_delete=models.CASCADE,
                                verbose_name="Рассылка")
    last_attempt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUSES, verbose_name="Статус отправки")
    server_response = models.TextField(**NULLABLE, verbose_name="Ответ почтового сервера")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("status", "last_attempt")

    def __str__(self):
        return f"Попытка №{self.pk} для рассылки №{self.mailing.pk}, статус: {self.status}"
