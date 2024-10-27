from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.auth.hashers import make_password
from users.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from config.settings import EMAIL_HOST_USER
import secrets
from users.utils import generate_random_password


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Вы оставили заявку на регистрацию на сайте {host}. '
                    f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserPasswordResetView(PasswordResetView):
    """ Контроллер восстановления пароля """
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message=f"Ваш новый пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            messages.success(self.request, 'Ваш пароль был успешно изменен!')
            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            messages.warning(self.request, 'Пользователя, зарегистрированного с таким email, на сайте нет!')

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """ Контроллер изменения пароля """
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль был успешно изменен!')
        return super().form_valid(form)
