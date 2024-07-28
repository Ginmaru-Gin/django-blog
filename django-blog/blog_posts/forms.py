from django import forms

class CreatePostForm(forms.Form):
    header = forms.CharField(label="Заголовок", max_length=80)
    text = forms.CharField(label="Текст", max_length=200, widget=forms.Textarea())
