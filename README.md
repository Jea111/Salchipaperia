# Salchipaperia

Aplicación web de ejemplo (Django) para un pequeño restaurante/punto de venta.

## Descripción

Proyecto Django sencillo que maneja categorías y productos, permite registrar clientes (usuarios) y guardar pedidos. 

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt` 

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
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Ejecutar servidor local:

```powershell
python manage.py runserver
```



## Rutas principales

- '/' inicio de la pagina con todos los productos
- 'pedidos/' se registra el pedido y se redirige a un form para crear el pedido con un usuario relacionado
- 'resenas/' deja tu sugerencia o queja de la web ( me llega un email al correo admin laliendra42@gmail.com)

