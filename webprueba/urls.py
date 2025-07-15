from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Para cerrar sesión
from django.shortcuts import redirect
from usuarios import views as usuarios_views
from usuarios.views import RegistroView

urlpatterns = [
    path('', lambda request: redirect('index'), name='index'),  # Redirige la raíz al login
    path('admin/', admin.site.urls),  # Panel de administración

    # Usuarios
    path('login/', usuarios_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('index/', usuarios_views.index_view, name='index'),
    path('tabla/', usuarios_views.user_list, name='user_list'),
    path('registro/', RegistroView.as_view(), name='registro'),
    #path('registro/', usuarios_views.registro, name='registro'),
    #path('registro/<int:user_id>/', usuarios_views.registro, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', usuarios_views.eliminar_usuario, name='eliminar_usuario'),
    path('contactos/', include('contactos.urls')),
    

    # Pedidos
    path('pedidos/', include('pedidos.urls')),
]
