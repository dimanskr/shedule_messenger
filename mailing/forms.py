from django import forms

from mailing.models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

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


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('clients', 'message', 'start_datetime', 'periodicity',)

        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Устанавливаем статус "Создана" при каждом изменении рассылки
        mailing = super().save(commit=False)
        mailing.status = 'created'
        if commit:
            mailing.save()
        return mailing
