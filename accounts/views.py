from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def cadastro(request):
    if request.method != 'POST':
        messages.info(request, 'Nada postado')
        return render(request, 'accounts/cadastro.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    repetir_senha = request.POST.get('repetir_senha')

    if not usuario or not senha or not repetir_senha:
        messages.error(request, 'Há campos que não foram preenchidos')
        return render(request, 'accounts/cadastro.html')

    email = request.POST.get('email')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/cadastro.html')

    if repetir_senha != senha:
        messages.error(request, 'Senhas com discordacias de caracteres')
        return render(request, 'accounts/cadastro.html')

    if ' ' in senha:
        messages.error(request, 'Senha não pode conter espaços')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 8:
        messages.error(request, 'Senha não pode conter menos de 8 caracteres')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'usuário já existente')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso!Faça seu login')
    user = User.objects.create_user(
        username=usuario, email=email, password=senha)
    user.save()
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
