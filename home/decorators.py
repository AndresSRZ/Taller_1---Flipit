from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_with_message(message="Debes iniciar sesión para acceder a esta funcionalidad."):
    """
    Decorador que verifica si el usuario está autenticado y muestra un mensaje personalizado si no lo está.
    
    Args:
        message: Mensaje a mostrar si el usuario no está autenticado
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, message)
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def add_message(message_type, message_text):
    """
    Decorador que añade un mensaje al request después de ejecutar la vista.
    
    Args:
        message_type: Tipo de mensaje (success, error, info, warning)
        message_text: Texto del mensaje
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            getattr(messages, message_type)(request, message_text)
            return response
        return wrapper
    return decorator

def confirm_action(confirmation_message, cancel_url):
    """
    Decorador que solicita confirmación antes de ejecutar una acción.
    
    Args:
        confirmation_message: Mensaje de confirmación
        cancel_url: URL a la que redirigir si se cancela la acción
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.GET.get('confirmed') == 'true':
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, confirmation_message)
                return redirect(f"{request.path}?confirmed=true")
        return wrapper
    return decorator

def track_user_activity(activity_description):
    """
    Decorador que registra la actividad del usuario.
    
    Args:
        activity_description: Descripción de la actividad
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Aquí se podría implementar un registro de actividad
                # Por ejemplo, guardar en una tabla de la base de datos
                print(f"Usuario {request.user.username} realizó: {activity_description}")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
