from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.views.generic.edit import FormView
from django.utils.http import urlencode
from django.views import View
from .models import Pedido, Ruta
from .forms import PedidoForm, RutaForm

import googlemaps
from itertools import permutations
import urllib.parse

API_KEY = 'AIzaSyC3P7JedZwrkvQUVjTXgdBEm7Nx4YwpFvE'


# --- PEDIDOS --- #

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedido_list.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        txtbusqueda = self.request.GET.get('txtbusqueda')
        queryset = Pedido.objects.filter(id_usuario=self.request.user, id_ruta__isnull=True).exclude(estado='Entregado')
        if txtbusqueda:
            queryset = queryset.filter(direccion__icontains=txtbusqueda)
            
        # Reemplazar primer caracter del código postal
        for pedido in queryset:
            pedido.codigo_postal = pedido.codigo_postal[1:]
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedidos_entregados = Pedido.objects.filter(id_usuario=self.request.user, estado='Entregado')
        # print(Pedido.objects.filter(id_usuario=self.request.user).values('id_pedido', 'estado'))
        # context['pedidos_entregados'] = pedidos_entregados
        
        for pedido in pedidos_entregados:
            pedido.codigo_postal = ''.join(filter(str.isdigit, pedido.codigo_postal))

        context['pedidos_entregados'] = pedidos_entregados
        return context



class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    template_name = 'pedido_form.html'
    fields = ['direccion', 'codigo_postal']
    success_url = reverse_lazy('pedido_list')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        return super().form_valid(form)


class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido_form.html'
    success_url = reverse_lazy('pedido_list')

    def get_queryset(self):
        return Pedido.objects.filter(id_usuario=self.request.user)

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['tipo_objeto'] = 'pedido'
         return context
    

class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'bade_delete_view.html'
    success_url = reverse_lazy('pedido_list')

    def get_queryset(self):
        return Pedido.objects.filter(id_usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = 'pedido'
        return context

    

# --- RUTAS --- #

@login_required
def crear_ruta(request):
    if request.method == 'POST':
        nombre_ruta = request.POST.get('nombre_ruta')
        pedido_ids = request.POST.getlist('pedido_ids')

        if not nombre_ruta or not pedido_ids:
            messages.error(request, "Debe ingresar un nombre y seleccionar al menos un pedido.")
            return redirect('pedido_list')

        nueva_ruta = Ruta.objects.create(nombre=nombre_ruta, id_usuario=request.user)
        Pedido.objects.filter(id_pedido__in=pedido_ids).update(id_ruta=nueva_ruta)

        messages.success(request, "Ruta creada exitosamente.")
        return redirect('ruta_list')
    return redirect('pedido_list')

class RutasListView(LoginRequiredMixin, ListView):
    model = Ruta
    template_name = 'ruta_list.html'

    def get_queryset(self):
        return Ruta.objects.filter(id_usuario=self.request.user).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        context['rutas_activas'] = Ruta.objects.filter(
            id_usuario=usuario, estado='activa'
        ).distinct()

        context['rutas_finalizadas'] = Ruta.objects.filter(
            id_usuario=usuario, estado__in=['Cancelada', 'Terminada']
        ).distinct()

        return context
    
class RutaUpdateView(LoginRequiredMixin, UpdateView):
    model = Ruta
    form_class = RutaForm
    template_name = 'ruta_form.html'
    success_url = reverse_lazy('ruta_list')

    def get_queryset(self):
        return Ruta.objects.filter(id_usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = 'ruta'

        # Agregar los pedidos relacionados a la ruta actual
        ruta = self.object  # ruta que se está editando
        context['pedidos'] = ruta.pedidos.all()  # gracias a related_name='pedidos'
        
        for pedido in context['pedidos']:
            pedido.codigo_postal = ''.join(filter(str.isdigit, pedido.codigo_postal))
            
        return context

# Quitar pedido de la ruta
def quitar_de_ruta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    ruta_id = pedido.id_ruta.id_ruta  # guardamos el ID de la ruta antes de desvincularlo

    pedido.id_ruta = None
    pedido.save()

    return redirect('ruta_edit', pk=ruta_id)
  
# Vista para eliminar ruta
class RutaDeleteView(LoginRequiredMixin, View):
    template_name = 'bade_delete_view.html'
    success_url = reverse_lazy('ruta_list')

    def get(self, request, pk):
        ruta = get_object_or_404(Ruta, pk=pk, id_usuario=request.user)
        return render(request, self.template_name, {'object': ruta, 'tipo_objeto': 'ruta'})

    def post(self, request, pk):
        ruta = get_object_or_404(Ruta, pk=pk, id_usuario=request.user)
        pedidos = ruta.pedidos.all()
        entregados = pedidos.filter(estado='Entregado')
        pendientes = pedidos.filter(estado='Pendiente')

        if not entregados.exists():
            # No hay entregados: se puede eliminar la ruta y liberar pedidos
            pendientes.update(id_ruta=None)
            ruta.delete()
            messages.success(request, "Ruta eliminada correctamente. Los pedidos pendientes fueron liberados.")
        else:
            # Hay entregados: cancelar la ruta y liberar pedidos pendientes
            pendientes.update(id_ruta=None)
            ruta.estado = 'Cancelada'
            ruta.save()
            messages.success(request, "Ruta cancelada correctamente. Los pedidos pendientes fueron liberados.")
        
        return redirect(self.success_url)

# --- MAPA --- #

def obtener_ruta_optima_google(inicio, destinos):
    gmaps = googlemaps.Client(key=API_KEY)
    response = gmaps.directions(
        origin=inicio,
        destination=inicio,
        waypoints=['optimize:true'] + destinos,
        mode="driving",
        region="ar"
    )

    if not response:
        return None

    leg = response[0]['legs']
    total_distancia = sum(segment['distance']['value'] for segment in leg)
    total_duracion = sum(segment['duration']['value'] for segment in leg)

    # reconstruir el orden optimizado
    waypoints_orden = response[0].get('waypoint_order', [])
    ruta_ordenada = [inicio] + [destinos[i] for i in waypoints_orden] + [inicio]

    return {
        'ruta': ruta_ordenada,
        'distancia_m': total_distancia,
        'duracion_s': total_duracion
    }



def generar_link_embed(ruta):
    base_url = "https://www.google.com/maps/embed/v1/directions"
    params = {
        'key': API_KEY,
        'origin': ruta[0],
        'destination': ruta[-1]
    }
    if len(ruta) > 2:
        params['waypoints'] = '|'.join(ruta[1:-1])
    return f"{base_url}?{urllib.parse.urlencode(params)}"



@login_required
def generar_mapa(request):
    id_ruta = request.POST.get('id_ruta') or request.GET.get('id_ruta')
    inicio_ruta = request.POST.get('inicio_ruta') or request.GET.get('inicio_ruta')

    if id_ruta and inicio_ruta:
        try:
            ruta = Ruta.objects.get(pk=id_ruta)
            ruta.inicio = inicio_ruta
            ruta.save()
            print(ruta.inicio)
            pedidos = ruta.pedidos.all()

            if request.method == 'POST':
                if 'guardar' in request.POST:
                    for pedido in pedidos:
                        estado = request.POST.get(f'estado_{pedido.id_pedido}')
                        if estado and estado in ['Pendiente', 'Entregado']:
                            pedido.estado = estado
                            pedido.save()

                    if all(p.estado == 'Entregado' for p in pedidos):
                        # Mostrar confirmación si aún no se envió decisión
                        return render(request, 'confirmar_terminada.html', {
                            'ruta': ruta,
                            'id_ruta': id_ruta,
                            'inicio_ruta': inicio_ruta,
                        })

                    messages.success(request, "Estados actualizados correctamente.")
                    params = urlencode({'id_ruta': id_ruta, 'inicio_ruta': inicio_ruta})
                    return HttpResponseRedirect(f"{reverse('generar_mapa')}?{params}")

                elif 'confirmar_terminada' in request.POST:
                    ruta.estado = 'Terminada'
                    ruta.save()
                    messages.success(request, "Ruta marcada como terminada.")
                    return redirect('ruta_list')

                elif 'cancelar_terminada' in request.POST:
                    messages.info(request, "Ruta no fue marcada como terminada.")
                    params = urlencode({'id_ruta': id_ruta, 'inicio_ruta': inicio_ruta})
                    return HttpResponseRedirect(f"{reverse('generar_mapa')}?{params}")

            # Armado de la ruta original
            direcciones = [f"{p.direccion}" for p in pedidos]
            direcciones_original = [f"{p.direccion}" for p in pedidos]
            direcciones_original.insert(0, inicio_ruta)
            direcciones_original.append(inicio_ruta)

            if len(direcciones) < 2:
                return render(request, 'ruta_list.html', {
                    'error': "Se necesitan al menos dos direcciones para calcular la ruta.",
                })

            gmaps = googlemaps.Client(key=API_KEY)
            distancia_original = 0
            duracion_original = 0
            for i in range(len(direcciones_original) - 1):
                res = gmaps.distance_matrix(direcciones_original[i], direcciones_original[i + 1], mode="driving", region="ar")
                elemento = res['rows'][0]['elements'][0]
                distancia_original += elemento['distance']['value']
                duracion_original += elemento['duration']['value']

            # Ruta optimizada
            resultado_optima = obtener_ruta_optima_google(inicio_ruta, direcciones)
            distancia_opt = resultado_optima['distancia_m']
            duracion_opt = resultado_optima['duracion_s']
            ruta_optima = resultado_optima['ruta']

            # Mejoras
            mejora_distancia = (1 - distancia_opt / distancia_original) * 100
            mejora_duracion = (1 - duracion_opt / duracion_original) * 100

            mapa_url = generar_link_embed(ruta_optima)

            # Lista de pedidos ordenados
            pedidos_ordenados = []
            for direccion in ruta_optima:
                if direccion == inicio_ruta:
                    continue
                pedido = pedidos.filter(direccion=direccion).first()
                if pedido:
                    pedidos_ordenados.append(pedido)

            return render(request, 'mapa.html', {
                'ruta_select': ruta,
                'pedidos_ruta': pedidos,
                'pedidos_ordenados': pedidos_ordenados,
                'mapa_url': mapa_url,
                'ruta_original': direcciones_original,
                'distancia_original': round(distancia_original / 1000, 2),
                'duracion_original': round(duracion_original / 60, 2),
                'ruta_optima': ruta_optima,
                'distancia_km': round(distancia_opt / 1000, 2),
                'duracion_min': round(duracion_opt / 60, 2),
                'mejora_distancia': round(mejora_distancia, 2),
                'mejora_duracion': round(mejora_duracion, 2),
            })

        except Ruta.DoesNotExist:
            return render(request, 'ruta_list.html', {
                'error': "Ruta no encontrada.",
            }, status=404)
        

def ruta_listado(request):
    rutas_activas = Ruta.objects.filter(estado='Activa')
    rutas_finalizadas = Ruta.objects.filter(estado__in=['Terminada', 'Cancelada'])

    return render(request, 'ruta_list.html', {
        'rutas_activas': rutas_activas,
        'rutas_finalizadas': rutas_finalizadas,
    })

def ruta_detalle(request, id_ruta):
    try:
        ruta = get_object_or_404(Ruta, pk=id_ruta)
        pedidos = Pedido.objects.filter(id_ruta=ruta)
        
        inicio_ruta = ruta.inicio

        # Ruta original
        direcciones = [p.direccion for p in pedidos]
        direcciones_original = [inicio_ruta] + direcciones + [inicio_ruta]

        gmaps = googlemaps.Client(key=API_KEY)
        distancia_original = 0
        duracion_original = 0
        for i in range(len(direcciones_original) - 1):
            res = gmaps.distance_matrix(direcciones_original[i], direcciones_original[i + 1], mode="driving", region="ar")
            elemento = res['rows'][0]['elements'][0]
            distancia_original += elemento['distance']['value']
            duracion_original += elemento['duration']['value']

        # Ruta optimizada
        resultado_optima = obtener_ruta_optima_google(inicio_ruta, direcciones)
        distancia_opt = resultado_optima['distancia_m']
        duracion_opt = resultado_optima['duracion_s']
        ruta_optima = resultado_optima['ruta']

        mejora_distancia = (1 - distancia_opt / distancia_original) * 100
        mejora_duracion = (1 - duracion_opt / duracion_original) * 100

        mapa_url = generar_link_embed(ruta_optima)

        pedidos_ordenados = []
        for direccion in ruta_optima:
            if direccion == inicio_ruta:
                continue
            pedido = pedidos.filter(direccion=direccion).first()
            if pedido:
                pedidos_ordenados.append(pedido)

        return render(request, 'ruta_detalle.html', {
            'ruta_select': ruta,
            'pedidos_ruta': pedidos,
            'pedidos_ordenados': pedidos_ordenados,
            'mapa_url': mapa_url,
            'ruta_original': direcciones_original,
            'distancia_original': round(distancia_original / 1000, 2),
            'duracion_original': round(duracion_original / 60, 2),
            'ruta_optima': ruta_optima,
            'distancia_km': round(distancia_opt / 1000, 2),
            'duracion_min': round(duracion_opt / 60, 2),
            'mejora_distancia': round(mejora_distancia, 2),
            'mejora_duracion': round(mejora_duracion, 2),
        })
    except Exception as e:
        return render(request, 'ruta_list.html', {
            'error': f"Ocurrió un error: {str(e)}",
        }, status=500)
        
class RutaCancelada(LoginRequiredMixin, DetailView):
    model = Ruta
    template_name = 'ruta_form.html'
    context_object_name = 'ruta'  # accedes como {{ ruta }} en la plantilla

    def get_queryset(self):
        return Ruta.objects.filter(id_usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ruta = self.get_object()

        # Obtener solo los pedidos entregados
        pedidos_entregados = ruta.pedidos.filter(estado='Entregado')

        context['pedidos'] = pedidos_entregados
        
        for pedido in context['pedidos']:
            pedido.codigo_postal = ''.join(filter(str.isdigit, pedido.codigo_postal))
        
        context['tipo_objeto'] = 'ruta_cancelada'
        return context