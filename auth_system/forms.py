from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm
from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import SetPasswordForm

from django import forms

from .utils import HashTable

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
        return HashTable(self.fields)


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
        return HashTable(self.fields)




class MyChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'placeholder': 'Старий пароль',
            'class': 'shadow-default'
        })
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
        return HashTable(self.fields


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'shadow-default'
        self.fields['password2'].widget.attrs['class'] = 'shadow-default'
        return HashTable(self.fields



class MySocialSignupForm(SocialSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'shadow-default', 'placeholder': 'Ел. Пошта'})
        return HashTable(self.fields


class ReviewForm(forms.Form):
    content = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'class': 'shadow-default',
        'placeholder': 'Введіть Ваш відгук',
    }), label='Відгук')
    stars = forms.IntegerField(label='Оцінка', widget=forms.TextInput(attrs={
        'class': 'shadow-default',
        'placeholder': 'Оцінка від 1 до 10',
    }))

    def clean_stars(self):
        value = self.cleaned_data['stars']
        if value < 1 or value > 10:
            raise forms.ValidationError('Оцінка повинна бути в діапазоні від 1 до 10')
        return value
