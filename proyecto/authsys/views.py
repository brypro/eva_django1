from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm 
from django.http import HttpResponse
from .models import CustomUser

# Vista de registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
        else:
            messages.error(request, "Por favor corrige los errores señalados.")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'authsys/register.html', {'form': form})

# Vista de login de usuarios
def login_view(request):
     if 'login_attempts' not in request.session:
        request.session['login_attempts'] = 0

     if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                # Verificamos si el usuario existe en la base de datos
                user_check = CustomUser.objects.get(username=username)
                if user_check.is_blocked:
                    messages.error(request, "Esta cuenta está bloqueada.")
                    return render(request, 'authsys/login.html', {'form': form})
            except CustomUser.DoesNotExist:
                # Si el usuario no existe, mostramos un mensaje de error
                messages.error(request, "El usuario no existe.")
                return render(request, 'authsys/login.html', {'form': form})

            # Intentamos autenticar al usuario
            user = authenticate(username=username, password=password)

            if user is not None:
                request.session['login_attempts'] = 0
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                return redirect('welcome')
            else:
                request.session['login_attempts'] += 1
                if request.session['login_attempts'] >= 3:
                    user_check.is_blocked = True
                    user_check.save()
                    messages.error(request, "Tu cuenta ha sido bloqueada tras tres intentos fallidos.")
                else:
                    messages.error(request, f"Usuario o contraseña incorrectos. Intentos fallidos: {request.session['login_attempts']}")
        else:
            messages.warning(request, "Por favor ingresa tanto el nombre de usuario como la contraseña.")
        
        return render(request, 'authsys/login.html', {'form': form})

     else:
        form = AuthenticationForm()

     return render(request, 'authsys/login.html', {'form': form})

# Vista de bienvenida para usuarios autenticados
def welcome_view(request):
    if request.user.is_authenticated:  # Verificamos si el usuario está logueado
        return render(request, 'authsys/welcome.html')
    else:
        return redirect('login')  # Redirige al login si no está autenticado


def unlock_accounts(request):
    CustomUser.objects.filter(is_blocked=True).update(is_blocked=False)
    return HttpResponse("Todas las cuentas han sido desbloqueadas.")