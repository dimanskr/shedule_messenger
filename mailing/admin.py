from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment')
    list_filter = ('full_name', 'email')
    search_fields = ('full_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_datetime', 'periodicity', 'status')
    list_filter = ('status', 'periodicity')
    search_fields = ('message__text',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'last_attempt', 'status', 'server_response')
    list_filter = ('status',)
    search_fields = ('mailing',)

