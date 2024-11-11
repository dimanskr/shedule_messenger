from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from config.settings import OBJECTS_ON_PAGE_COUNT
from mailing.forms import ClientForm, MessageForm, MailingForm, ManagerMailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class PermissionFilteredQuerysetMixin(LoginRequiredMixin):
    """
    Миксин для get_queryset на основе разрешений пользователя
    """
    permission_name = None
    filter_field = 'author'

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает набор запросов на основе наличия у пользователя указанного разрешения
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user

        # Разрешить доступ ко всем объектам, если у пользователя есть необходимое разрешение
        if self.permission_name and user.has_perm(self.permission_name):
            return queryset

        # В противном случае отфильтруйте набор запросов по указанному полю и текущему пользователю
        if user.is_authenticated:
            filter_kwargs = {self.filter_field: user}
            return queryset.filter(**filter_kwargs)

        return queryset.none()


class ClientListView(PermissionFilteredQuerysetMixin, ListView):
    model = Client
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "client_list"


class ClientDetailView(PermissionFilteredQuerysetMixin, DetailView):
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


class MessageListView(PermissionFilteredQuerysetMixin, ListView):
    model = Message
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "message_list"


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


class MailingListView(PermissionFilteredQuerysetMixin, ListView):
    model = Mailing
    paginate_by = OBJECTS_ON_PAGE_COUNT
    context_object_name = "mailing_list"
    permission_name = 'mailing.can_watch_mailing'


class MailingDetailView(PermissionFilteredQuerysetMixin, DetailView):
    model = Mailing
    permission_name = 'mailing.can_watch_mailing'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.author = self.request.user
        mailing.save()
        form.instance.clients.set(self.request.POST.getlist("clients"))
        messages.success(self.request, 'Рассылка создана!')
        return super().form_valid(form)

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

    def get_form_class(self):
        current_user = self.request.user
        if current_user == self.object.author:
            return MailingForm
        if current_user.has_perm('mailing.can_deactivate_mailing'):
            return ManagerMailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка удалена!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if (
                mailing.author == request.user
                or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("У Вас нет прав на удаление рассылки.")


class MailingAttemptListView(PermissionFilteredQuerysetMixin, ListView):
    model = MailingAttempt
    paginate_by = OBJECTS_ON_PAGE_COUNT * 2
    context_object_name = "attempt_list"
    permission_name = 'mailing.can_watch_attempts'
    filter_field = 'mailing__author'
