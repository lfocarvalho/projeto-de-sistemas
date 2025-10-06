from django.views.generic import View
from django.shortcuts import redirect, render 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User

class Login(View):

    def get(self, request):
        contexto = {}
        return render(request, 'autenticacao.html', contexto)     
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
             if user.is_active:
                login(request, user)
                return redirect("/loja")
             
        
        return render(request, 'autenticacao.html', {'mensagem': 'Login Falhou!'})
    
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')
    

    def get(self, request):
        logout(request)
        return redirect('/')

class Cadastro(View):

    def get(self, request):
        return render(request, 'cadastro.html')
    
    def post(self, request):
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        if senha != senha2:
            return render(request, 'cadastro.html', {'mensagem': 'As senhas não coincidem.'})

        user = User.objects.create_user(username=usuario, email=email, password=senha)
        user.save()
        return redirect('login')
