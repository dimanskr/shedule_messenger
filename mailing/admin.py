from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment', 'author')
    list_filter = ('full_name', 'email')
    search_fields = ('full_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'author')
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_datetime', 'periodicity', 'status', 'is_active', 'author')
    list_filter = ('status', 'periodicity', 'is_active')
    search_fields = ('message__text',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'last_attempt', 'status', 'server_response', 'mailing__is_active')
    list_filter = ('status',)
    search_fields = ('mailing',)

