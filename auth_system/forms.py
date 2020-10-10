from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm

from django import forms


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'shadow-default', 'placeholder': 'Ел. Пошта'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'shadow-default', 'placeholder': 'Пароль'})


class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'shadow-default', 'placeholder': 'Ел. Пошта'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'shadow-default', 'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'shadow-default', 'placeholder': 'Повтор паролю'})


class MyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={
            "type": "email",
            "size": "30",
            "placeholder": 'Ел. Пошта',
            "class": 'shadow-default'
        })


class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(MyResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'placeholder': 'Новий пароль',
            'class': 'shadow-default'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'placeholder': 'Повтор паролю',
            'class': 'shadow-default'
        })
