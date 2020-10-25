from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
banned_users = ["Donald Trump", "FBI"]

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    def clean(self):
        data = super().clean()
        username = data.get("username")
        password = data.get("password")

    def clean_username(self):
            username = self.cleaned_data.get("username")
            qs = User.objects.filter(username__iexact=username)
            if username in banned_users:
                raise forms.ValidationError("This is an invalid username, please pick another.")
            if qs.exists():
                raise forms.ValidationError("This is not an valid user.")
            return username
            
    def clean_email(self):
            email = self.cleaned_data.get("email")
            qs = User.objects.filter(email__iexact=email)
            if qs.exists():
                raise forms.ValidationError("This email is already in use, please pick another.")
            return email

    def clean_password(self):
            password = self.cleaned_data.get("password")
            confirm_password = self.cleaned_data.get("confirm_password")
            if password != confirm_password:
                raise forms.ValidationError("The passwords dont match.")
            return password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

