from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Article
UserModel = get_user_model()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class LoginViewForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }
    ))

    def clean(self):
        if not authenticate(**self.cleaned_data):
            raise ValidationError('Incorrect username or password.')


class RegisterViewForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            'placeholder': 'Email',
            'class': 'form-control',
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }
    ))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }
    ))

    def clean(self):
        username = self.cleaned_data['username']
        try:
            UserModel.objects.get(username=username)
            self.add_error('username', 'User with this username already exist.')
        except UserModel.DoesNotExist:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                self.add_error('password', 'Password does not match.')
                self.add_error('confirm_password', 'Confirm password does not match.')

    def create_user(self):
        del self.cleaned_data['confirm_password']
        UserModel.objects.create_user(**self.cleaned_data)


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password:')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password:')

    class Meta:
        model = User
        fields = ('new_password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            self.add_error("new_password", "Does not match")
            self.add_error("confirm_password", "Does not match")

    def change_password(self, user):
        password = self.cleaned_data["new_password"]
        user.set_password(password)
        user.save()


class ChangeUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'