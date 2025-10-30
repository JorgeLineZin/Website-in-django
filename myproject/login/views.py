from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


def login_home(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
            else:
                # Erro genérico para não revelar se email existe
                form.add_error(None, "Email ou senha incorretos.")
        # Se inválido, re-renderiza com erros
        return render(request, "index/login.html", {"form": form})

    # GET
    return render(request, "index/login.html", {"form": LoginForm()})


def register_home(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data.get("first_name", "")
            last_name = form.cleaned_data.get("last_name", "")
            # Cria usuário com senha criptografada (hash) via create_user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            # Autentica e faz login após cadastro
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
            return redirect("/login/")
        # Se inválido, re-renderiza com erros
        return render(request, "index/register.html", {"form": form})

    # GET
    return render(request, "index/register.html", {"form": RegisterForm()})


def logout_view(request):
    """Encerra a sessão do usuário e redireciona para a home."""
    auth_logout(request)
    return redirect("/")