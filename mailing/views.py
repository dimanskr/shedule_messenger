from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from config.settings import OBJECTS_ON_PAGE_COUNT
from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientListView(ListView):
    model = Client
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "client_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(author=user)

        return queryset.none()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.author = user
        client.save()
        messages.success(self.request, 'Клиент успешно создан!')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные о клиенте изменены!')
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные о клиенте удалены!')
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "message_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(author=user)

        return queryset.none()


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.author = user
        message.save()
        messages.success(self.request, 'Сообщение создано!')
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        messages.success(self.request, 'Сообщение изменено!')
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        messages.success(self.request, 'Сообщение удалено!')
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "mailing_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(author=user)

        return queryset.none()


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(author=user)

        return queryset.none()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.author = user
        mailing.save()
        messages.success(self.request, 'Рассылка создана!')
        return super().form_valid(form)

        # Привязка выбранных клиентов после сохранения формы
        clients_ids = self.request.POST.getlist("clients")
        form.instance.clients.set(clients_ids)

    def get_form_kwargs(self):
        """
        Получаем доступ к queryset для фильтрации данных выводимых в форму рассылки
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка успешно изменена!')
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Получаем доступ к queryset для фильтрации данных выводимых в форму рассылки
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка удалена!')
        return super().form_valid(form)


class MailingAttemptListView(ListView):
    model = MailingAttempt
    paginate_by = OBJECTS_ON_PAGE_COUNT * 2
    context_object_name = "attempt_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(mailing__author=user)

        return queryset.none()
