import re
from django import forms
from django.contrib.auth.models import User


EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Email inválido.")
        return email


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Nome", required=False)
    last_name = forms.CharField(label="Sobrenome", required=False)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Email inválido.")
        # Verifica se já existe usuário com este email (em username ou email)
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email já cadastrado.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get("password", "")
        # Regras simples: mínimo 8, pelo menos 1 letra e 1 dígito
        if len(pwd) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Za-z]", pwd):
            raise forms.ValidationError("A senha deve conter letras.")
        if not re.search(r"\d", pwd):
            raise forms.ValidationError("A senha deve conter números.")
        return pwd

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        pwd2 = cleaned.get("password2")
        if pwd and pwd2 and pwd != pwd2:
            self.add_error("password2", "As senhas não coincidem.")
        return cleaned