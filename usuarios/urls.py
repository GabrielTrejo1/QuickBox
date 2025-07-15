from django.urls import path
from . import views
from .views import RegistroView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('tabla/', views.user_list, name='user_list'),
    #path('registro/', views.registro, name='registro'),
    path('registro/', RegistroView.as_view(), name='registro'),
    #path('registro/<int:user_id>/', views.registro, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
