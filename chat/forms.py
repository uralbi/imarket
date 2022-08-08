from django import forms
from .models import Chat


class Chat_Form(forms.ModelForm):
    content = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'row': 4, 'col': 4}))

    class Meta:
        model = Chat
        fields = ['sender', 'receiver', 'subject', 'content']