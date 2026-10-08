from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import CustomUser


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class CustomUserCreationForm(UserCreationForm):
    # username = forms.CharField(
    #     label="Логін",
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )

    email = forms.EmailField(
        label="Електронна пошта",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        label="Ім'я",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Вкажіть ім'я"})
    )

    last_name = forms.CharField(
        label="Прізвище",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        label="Зображення",
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="Пароль",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label="Повторіть пароль",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'image', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Дана пошта уже зареєстрована")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")
        return password2