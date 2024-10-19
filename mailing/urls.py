from mailing.apps import MailingConfig
from django.urls import path, include

from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MailingListView, MailingDetailView, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, MailingAttemptListView

app_name = MailingConfig.name

urlpatterns = [
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path("client_edit/<int:pk>/", ClientUpdateView.as_view(), name="client_edit"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),

    path("messages/", MessageListView.as_view(), name="message_list"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_edit/<int:pk>/", MessageUpdateView.as_view(), name="message_edit"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),

    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing_edit/<int:pk>/", MailingUpdateView.as_view(), name="mailing_edit"),
    path("mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),

    path("mailing_logs/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
]

