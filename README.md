# 🚀 QuickBox

**QuickBox** es una aplicación web diseñada para organizar pedidos de reparto de forma eficiente. Permite a los usuarios generar rutas optimizadas, visualizar mapas interactivos e identificar mejoras en tiempo y distancia.

---

## 🧑‍💼 Acceso al sistema

- Requiere inicio de sesión para acceder a las funcionalidades.
- Cada usuario puede ver, editar o eliminar **solo sus propios** pedidos y rutas.

---

## 📋 Gestión de Pedidos

Desde la pantalla principal, el usuario puede:

- Ver pedidos **sin ruta asignada**.
- Agregar nuevos pedidos con **dirección** y **código postal**.
- **Modificar** pedidos existentes.
- **Eliminar** pedidos que ya no se necesiten.

> ⚠️ Los pedidos asignados a una ruta **no** se muestran en la pantalla principal.

---

## 🗺️ Creación de Rutas

- Los usuarios pueden **agrupar uno o más pedidos** en una ruta.
- Se debe asignar un **nombre** a cada ruta.
- Los pedidos seleccionados quedan automáticamente asociados a esa ruta.

---

## 🚚 Visualización de Rutas

Desde la sección de rutas, el usuario puede:

- Ver todas las rutas que ha creado.
- **Editar el nombre** de una ruta.
- **Eliminar una ruta** (los pedidos quedan nuevamente sin ruta).
- Ver un **mapa con la ruta optimizada**.

---

## 📍 Generar Mapa de Ruta

Al seleccionar una ruta y un punto de partida:

- El usuario puede marcar pedidos como **Entregado** o **Pendiente**.
- El sistema muestra:
  - El **recorrido original** (orden de carga).
  - La **ruta optimizada**, minimizando tiempo o distancia.
  - Un **mapa interactivo** con indicaciones (Google Maps).
  - **Comparativas** entre ruta original y optimizada:
    - Distancia total (km).
    - Duración estimada (minutos).
    - Porcentaje de mejora en tiempo y distancia.

---

## ✅ Resumen de Funcionalidades

| Funcionalidad      | Descripción                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Crear Pedido       | Cargar dirección y código postal de una entrega.                            |
| Editar Pedido      | Modificar los datos de un pedido ya creado.                                 |
| Eliminar Pedido    | Eliminar definitivamente un pedido.                                         |
| Crear Ruta         | Agrupar pedidos en una ruta con nombre.                                     |
| Ver Rutas          | Mostrar todas las rutas creadas por el usuario.                             |
| Editar Ruta        | Cambiar el nombre de la ruta.                                                |
| Eliminar Ruta      | Quitar la ruta (los pedidos vuelven a quedar sin asignar).                  |
| Generar Mapa       | Calcular y mostrar la mejor secuencia de entrega en un mapa interactivo.    |

---

## 🛠️ Tecnologías Utilizadas

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Django (Python)  
- **Base de datos**: MySQL / SQLite  
- **Mapas y rutas**: Google Maps API  
- **Autenticación**: Sistema de login por usuario  
- **Otros**: Bootstrap

---

## ⚙️ Instalación y Configuración

1. Cloná el repositorio:  
   `git clone https://github.com/GabrielTrejo1/QuickBox && cd quickbox`

2. Creá un entorno virtual:  
   `python -m venv env`

3. Activá el entorno virtual:  
   - En Linux/macOS: `source env/bin/activate`  
   - En Windows: `env\Scripts\activate`

4. Instalá dependencias:  
   `pip install -r requirements.txt`

5. Creá un archivo `.env` con las siguientes variables:  
   SECRET_KEY=tu_clave_secreta  
   DEBUG=True  
   GOOGLE_MAPS_API_KEY=tu_clave_de_api


6. Ejecutá migraciones:  
`python manage.py migrate`

7. (Opcional) Creá un usuario admin:  
`python manage.py createsuperuser`

8. Ejecutá el servidor de desarrollo:  
`python manage.py runserver`

9. Accedé a la app en:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)


