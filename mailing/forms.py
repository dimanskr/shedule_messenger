from django import forms

from mailing.models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('author',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('author',)

    prohibited_words_list = []  # список запрещенных слов заполним позже (при необходимости)

    def clean_subject(self):
        cleaned_data = self.cleaned_data['subject']

        for word in self.prohibited_words_list:
            if word in cleaned_data:
                raise forms.ValidationError('Запрещенные слова в теме письма!')

        return cleaned_data

    def clean_body(self):
        cleaned_data = self.cleaned_data['body']

        for word in self.prohibited_words_list:
            if word in cleaned_data:
                raise forms.ValidationError('Запрещенные слова в письме!')

        return cleaned_data


# class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
#     """
#     Кастомная модель множественного выбора
#     """
#     def label_from_instance(self, clients):
#         return "%s" % clients.email


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('clients', 'message', 'start_datetime', 'periodicity',)

        widgets = {
            'clients': forms.CheckboxSelectMultiple(),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Получаем доступ к queryset для фильтрации рассылки
        """
        curr_user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if curr_user:
            self.fields['clients'].queryset = Client.objects.filter(author=curr_user)
            self.fields['message'].queryset = Message.objects.filter(author=curr_user)
        else:
            self.fields['clients'].queryset = Client.objects.objects.none()
            self.fields['message'].queryset = Message.objects.objects.none()

    def save(self, commit=True):
        # Устанавливаем статус "Создана" при каждом изменении рассылки
        mailing = super().save(commit=False)
        mailing.status = 'created'
        if commit:
            mailing.save()
            self.save_m2m()
        return mailing
