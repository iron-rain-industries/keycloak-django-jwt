from django import forms

class RequestTokenForm(forms.Form):
    user_name = forms.CharField(max_length=256)
    user_pass = forms.CharField(max_length=64, widget=forms.PasswordInput)