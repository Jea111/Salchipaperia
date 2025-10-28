# Salchipaperia

Aplicación web de ejemplo (Django) para un pequeño restaurante/punto de venta.

## Descripción

Proyecto Django sencillo que maneja categorías y productos, permite registrar clientes (usuarios) y guardar pedidos. Incluye plantillas básicas (`inicio.html`, `login.html`) y soporte para imágenes (carpeta `media/`).

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt` (Django 5.2.4, Pillow, psycopg2, ...)

## Instalación y ejecución (PowerShell)

1. Sitúate en la carpeta del proyecto:


2. Crear y activar un entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt

5. Migraciones y superusuario:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

6. Ejecutar servidor local:

```powershell
python manage.py runserver
```

Abre http://127.0.0.1:8000/ en tu navegador.

## Estructura relevante

- `manage.py` — comandos admin de Django.
- `requirements.txt` — dependencias.
- `restaurante_proyecto/` — settings, urls, wsgi/asgi.
- `restaurante_app/` — modelos, vistas, templates y estáticos.
- `media/` — archivos subidos (configurado como MEDIA_ROOT).

## Rutas principales

- `/` → vista `users` (login/simple registro) — definida en `restaurante_app/urls.py`.
- `/inicio/` → vista `inicio` que lista productos.

