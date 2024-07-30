from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CreatePostForm(forms.Form):
    header = forms.CharField(label="Заголовок", max_length=80)
    text = forms.CharField(label="Текст", max_length=200, widget=forms.Textarea())


class SearchPostForm(forms.Form):
    author = forms.CharField(label="Поиск по авторам", max_length=200, required=False)
    header = forms.CharField(label="Поиск по заголовкам", max_length=80, required=False)
    text = forms.CharField(
        label="Поиск по текстам",
        max_length=200,
        required=False,
        widget=forms.Textarea(),
    )

    def clean(self):
        if not self.has_changed():
            pass
            raise ValidationError(_("All searching fields are emtpy!"))
