from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistroForm
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView


def login_view(request):
    next_page = request.GET.get('next', '/pedidos/')  # Recupera el "next" del GET para redirigir después del login

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():  # Verifica si el formulario es válido
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_page)  # Redirige a la página de inicio después de login exitoso
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")
        else:
            form.add_error(None, "Formulario no válido")
    
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')

def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')  # Redirige al index

@login_required
def tabla_view(request):
    return render(request, 'tabla.html')

#REGISTRO ECHO CON FUNCIONES
'''def registro(request, user_id=None):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            # Ya existe ese nombre de usuario
            return render(request, 'registro.html', {'error': 'El nombre de usuario ya existe'})
        
        if password != password2:
            return render(request, 'registro.html', {'error': 'Las contraseñas son distintas'})

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')  # Redirigís donde quieras

    return render(request, 'registro.html')'''

#REGISTRO CON CLASSES
class RegistroView(FormView):
    template_name = 'registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('login')  # Redirige al login después del registro

    def form_valid(self, form):
        # Crear el usuario
        User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        return super().form_valid(form)

@login_required
def user_list(request):
    # Obtener todos los usuarios
    users = User.objects.all()
    return render(request, 'tabla.html', {'users': users})

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Evitar que el usuario se elimine a sí mismo
    if request.user != user:
        user.delete()
        # Enviar una respuesta JSON con el ID del usuario eliminado
        return JsonResponse({'user_id': user_id})
    
    # Si no es posible eliminar al usuario, enviar un error
    return JsonResponse({'error': 'No puedes eliminarte a ti mismo'}, status=400)