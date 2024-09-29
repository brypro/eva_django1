
# Proyecto de Autenticación en Django

Este proyecto es una aplicación web desarrollada en Django que implementa un sistema de autenticación de usuarios, incluyendo un mecanismo para bloquear cuentas tras múltiples intentos fallidos de inicio de sesión, cierre de sesión seguro, y más.

## Características

- Registro de usuarios con validación de nombre de usuario y contraseña.
- Login con manejo de intentos fallidos (bloqueo de cuenta tras 3 intentos).
- Logout seguro utilizando el método POST.
- Gestión de usuarios autenticados con protección de vistas.
- Funcionalidad de desbloqueo de cuentas para propósitos de demo.

## Requisitos
- node (para tailwind)
- Python 3.x
- Django 5.x o superior
- Base de datos SQLite (por defecto) o cualquier otra base de datos soportada por Django

## Configuración del entorno

1. Clona el repositorio:

   ```bash
   git clone ...
   cd tu-repositorio
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instala las dependencias necesarias:

   * Desde \proyecto\authsys\static_src
      ```bash
      npm install
      ```
   * desde /proyecto
      ```bash
      pip install -r requirements.txt
      ```

4. Configura la base de datos y aplica las migraciones desde /proyecto:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Crea un superusuario para acceder al panel de administración:

   ```bash
   python manage.py createsuperuser
   ```

6. Inicia el manager de tailwind desde /proyecto:

   ```bash
   python manage.py tailwind start
   ```

7. Inicia el servidor de desarrollo desde /proyecto:

   ```bash
   python manage.py runserver
   ```

## Funcionalidades clave

### Registro de usuarios

Los usuarios pueden registrarse proporcionando un nombre de usuario, correo electrónico, y una contraseña que cumple con los siguientes requisitos:

- Mínimo de 8 caracteres
- Al menos una letra mayúscula
- Al menos un número

### Inicio de sesión (Login)

El sistema permite a los usuarios iniciar sesión utilizando su nombre de usuario y contraseña. Después de 3 intentos fallidos de autenticación, la cuenta será bloqueada.

### Bloqueo de cuentas

Si un usuario introduce credenciales incorrectas 3 veces, su cuenta será bloqueada. Puedes manejar este comportamiento en el código definido en `views.py`:

```python
# Ejemplo de bloqueo de cuenta tras 3 intentos fallidos
if request.session['login_attempts'] >= 3:
    user_to_block.is_blocked = True
    user_to_block.save()
    messages.error(request, "Tu cuenta ha sido bloqueada tras tres intentos fallidos.")
```

### Desbloqueo de cuentas

Para propósitos de demo, puedes desbloquear todas las cuentas bloqueadas accediendo a la siguiente URL:

```bash
http://localhost:8000/desbloquear/
```

### Cierre de sesión (Logout)

El logout se maneja de forma segura utilizando una solicitud **POST** para evitar cierres de sesión accidentales o no autorizados. Aquí está el código que debes usar en la vista de bienvenida (`welcome.html`):

```html
<form method="POST" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit" class="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded">
        Cerrar sesión
    </button>
</form>
```

### Rutas principales

- `/register/`: Página de registro de usuario.
- `/login/`: Página de inicio de sesión.
- `/logout/`: Cierra la sesión de usuario (requiere solicitud POST).
- `/welcome/`: Vista de bienvenida para usuarios autenticados.
- `/unlock/`: Desbloquea todas las cuentas bloqueadas (para demostraciones).

## Archivos importantes

- **`models.py`**: Contiene el modelo `CustomUser` que extiende el modelo de usuario de Django con un campo `is_blocked` para manejar el bloqueo de cuentas.
- **`views.py`**: Contiene la lógica de autenticación, bloqueo de cuentas, y el manejo de intentos fallidos.
- **`urls.py`**: Define las rutas para las vistas de login, registro, logout, y desbloqueo de cuentas.
- **`templates/`**: Contiene los archivos HTML para el frontend, incluyendo formularios de login, registro y la página de bienvenida.

## Panel de administración

Accede al panel de administración para gestionar usuarios y otros modelos en db:

```bash
http://localhost:8000/admin/
```

Asegúrate de haber creado un superusuario con el comando `createsuperuser` para poder acceder.

