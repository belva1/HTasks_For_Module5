from django import forms
from django.contrib.auth.models import User

from .models import Article
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # def save(self, commit=True):
    #     user_components = super().save(commit=False)
    #     user_components.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user_components.save()
    #     return user_components


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


class ChangeUserDataForm(UserChangeForm, forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
