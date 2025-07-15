# urls.py
from django.urls import path
from .views import *
from pedidos import views

urlpatterns = [
    path('', PedidoListView.as_view(), name='pedido_list'),
    path('crear/', PedidoCreateView.as_view(), name='pedido_create'),
    path('<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedido_edit'),
    path('<int:pk>/eliminar/', PedidoDeleteView.as_view(), name='pedido_delete'),
    path('<int:pk>/editar-ruta/', RutaUpdateView.as_view(), name='ruta_edit'),
    path('<int:pedido_id>/quitar/', views.quitar_de_ruta, name='quitar_de_ruta'),
    path('<int:pk>/eliminar-ruta/', RutaDeleteView.as_view(), name='ruta_delete'),
    path('rutas/', RutasListView.as_view(), name='ruta_list'),
    path('rutas/generar-mapa/', views.generar_mapa, name='generar_mapa'),
    path('crear-ruta/', crear_ruta, name='crear_ruta'),
    path('pedidos/rutas/<int:id_ruta>/terminada/', views.ruta_detalle, name='ruta_detalle'),
    path('pedidos/rutas/<int:pk>/ver/', RutaCancelada.as_view(), name='ruta_cancelada'),

]
