from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Prenda, Carrito
from .service_locator import ServiceLocator
from django.views.generic import ListView, FormView, RedirectView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

# Importar las interfaces y clases de los repositorios y servicios, antes de implementar singleton con
# la clase ServiceLocator para manejar la inyección de dependencias
"""
    from .interfaces import PrendaRepositoryInterface, CarritoRepositoryInterface, UserServiceInterface
    from .repositories import PrendaRepository, CarritoRepository, UserService
    from .services import PrendaFilterService

    # Inyección de dependencias
    prenda_repository: PrendaRepositoryInterface = PrendaRepository()
    carrito_repository: CarritoRepositoryInterface = CarritoRepository()
    user_service: UserServiceInterface = UserService()
    prenda_filter_service = PrendaFilterService(prenda_repository)
"""
# Home viejo
"""def home(request):
    # Filtro Nombre
    searchPrenda = request.GET.get("searchPrenda")
    prendas_nombre = Prenda.objects.all()
    if searchPrenda:
        prendas_nombre = prendas_nombre.filter(nombre__icontains=searchPrenda)
    
    # Filtro Precio
    precio = request.GET.get("precio")
    prendas_precio = Prenda.objects.all()
    if precio:
        try:
            precio = int(precio)
        except ValueError:
            prendas_precio = Prenda.objects.none()
        else:
            prendas_precio = prendas_precio.filter(precio__lte=precio)

    # Filtro Estado
    estado = request.GET.get("estado")
    prendas_estado = Prenda.objects.all()
    if estado:
        prendas_estado = prendas_estado.filter(estado__icontains=estado)
    # Filtro Talla
    talla = request.GET.get("talla")
    prendas_talla = Prenda.objects.all()
    if talla:
        prendas_talla = prendas_talla.filter(talla=talla)
    
    # Combinar resultados de todos los filtros
    prendas = prendas_nombre & prendas_precio & prendas_estado & prendas_talla
    
    # Obtener el carrito del usuario
    prendas_en_carrito = []
    total = 0
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        prendas_en_carrito = carrito.prendas.all()
        total = sum(prenda.precio for prenda in prendas_en_carrito)
    
    return render(request, 'home.html', {
        'searchPrenda': searchPrenda,
        'prendas': prendas,
        'precio': precio,
        'prendas_en_carrito': prendas_en_carrito,
        'total': total
    })
"""
# Vistas basadas en funciones
"""
def home(request):

    # Obtener servicios a través del ServiceLocator
    prenda_filter_service = ServiceLocator.get_prenda_filter_service()
    carrito_repository = ServiceLocator.get_carrito_repository()

    # Aplicar todos los filtros usando el servicio
    filter_params = {
        "searchPrenda": request.GET.get("searchPrenda"),
        "precio": request.GET.get("precio"),
        "estado": request.GET.get("estado"),
        "talla": request.GET.get("talla")
    }
    
    prendas = prenda_filter_service.apply_filters(filter_params)
    
    # Obtener el carrito del usuario
    prendas_en_carrito = []
    total = 0
    if request.user.is_authenticated:
        carrito, _ = carrito_repository.get_or_create_for_user(request.user)
        prendas_en_carrito = carrito_repository.get_prendas_in_carrito(carrito)
        total = carrito_repository.calculate_total(prendas_en_carrito)
    
    return render(request, 'home.html', {
        'searchPrenda': filter_params["searchPrenda"],
        'prendas': prendas,
        'precio': filter_params["precio"],
        'prendas_en_carrito': prendas_en_carrito,
        'total': total
    })

def registro(request):
    return render(request, 'registro.html')

def process_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nombre de usuario ya existe")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        messages.success(request, "Registro exitoso")
        return redirect('home')
    else:
        return redirect('registro')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('home')
            else:
                messages.error(request, "El usuario o la contraseña no son válidos")
        else:
            messages.error(request, "El usuario o la contraseña no son válidos")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente")
    return redirect('home')

def agregar_al_carrito(request, prenda_id):
    if request.user.is_authenticated:
        prenda = Prenda.objects.get(id=prenda_id)
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        carrito.prendas.add(prenda)
        messages.success(request, f'"{prenda.nombre}" se ha agregado al carrito.')
    else:
        messages.error(request, "Debes iniciar sesión para agregar prendas al carrito.")
    return redirect('home')

def ver_carrito(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        prendas_en_carrito = carrito.prendas.all()
        total = sum(prenda.precio for prenda in prendas_en_carrito)
        return render(request, 'carrito.html', {'prendas_en_carrito': prendas_en_carrito, 'total': total})
    else:
        messages.error(request, "Debes iniciar sesión para ver tu carrito.")
        return redirect('home')
    
def limpiar_carrito(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        carrito.prendas.clear()  # Esto eliminará todas las prendas del carrito
        messages.success(request, "El carrito se ha limpiado exitosamente.")
    else:
        messages.error(request, "Debes iniciar sesión para limpiar tu carrito.")
    return redirect('home')
"""

# Implementación del patrón Decorator
def message_decorator(message_type, message_text):
    """
    Decorador que añade un mensaje al request
    
    Args:
        message_type: Tipo de mensaje (success, error, etc.)
        message_text: Texto del mensaje
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            getattr(messages, message_type)(request, message_text)
            return response
        return wrapper
    return decorator

def login_required_message(view_func):
    """
    Decorador que verifica si el usuario está autenticado y muestra un mensaje si no lo está
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para acceder a esta funcionalidad.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vistas basadas en clases (implementación del patrón MTV)
class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'prendas'
    
    def get_queryset(self):
        # Obtener servicios a través del ServiceLocator
        prenda_filter_service = ServiceLocator.get_prenda_filter_service()
        
        # Aplicar todos los filtros usando el servicio
        filter_params = {
            "searchPrenda": self.request.GET.get("searchPrenda"),
            "precio": self.request.GET.get("precio"),
            "estado": self.request.GET.get("estado"),
            "talla": self.request.GET.get("talla")
        }
        
        return prenda_filter_service.apply_filters(filter_params)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito_repository = ServiceLocator.get_carrito_repository()
        
        # Añadir parámetros de filtro al contexto
        context['searchPrenda'] = self.request.GET.get("searchPrenda")
        context['precio'] = self.request.GET.get("precio")
        
        # Obtener el carrito del usuario
        prendas_en_carrito = []
        total = 0
        if self.request.user.is_authenticated:
            carrito, _ = carrito_repository.get_or_create_for_user(self.request.user)
            prendas_en_carrito = carrito_repository.get_prendas_in_carrito(carrito)
            total = carrito_repository.calculate_total(prendas_en_carrito)
        
        context['prendas_en_carrito'] = prendas_en_carrito
        context['total'] = total
        
        return context

class RegistroView(TemplateView):
    template_name = 'registro.html'

class ProcessRegistrationView(View):
    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Validaciones
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'registro.html', {
                'username': username, 
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email
            })
        
        user_service = ServiceLocator.get_user_service()
        
        if user_service.user_exists_by_username(username):
            messages.error(request, "Nombre de usuario ya existe")
            return render(request, 'registro.html', {
                'username': username, 
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email
            })
        
        if user_service.user_exists_by_email(email):
            messages.error(request, "El correo ya está registrado")
            return render(request, 'registro.html', {
                'username': username, 
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email
            })
        
        # Crear usuario
        user = user_service.create_user(
            username=username, 
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name
        )
        
        login(request, user)
        messages.success(request, "Registro exitoso")
        return redirect('home')
    
    def get(self, request):
        return redirect('registro')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user_service = ServiceLocator.get_user_service()
        user = user_service.authenticate_user(username, password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Inicio de sesión exitoso")
            return super().form_valid(form)
        else:
            messages.error(self.request, "El usuario o la contraseña no son válidos")
            return self.form_invalid(form)

class LogoutView(RedirectView):
    url = reverse_lazy('home')
    
    @method_decorator(message_decorator('success', "Sesión cerrada exitosamente"))
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class AgregarAlCarritoView(View):
    @method_decorator(login_required_message)
    def get(self, request, prenda_id):
        prenda_repository = ServiceLocator.get_prenda_repository()
        carrito_repository = ServiceLocator.get_carrito_repository()
        
        prenda = prenda_repository.get_by_id(prenda_id)
        carrito, _ = carrito_repository.get_or_create_for_user(request.user)
        carrito_repository.add_prenda_to_carrito(carrito, prenda)
        
        messages.success(request, f'"{prenda.nombre}" se ha agregado al carrito.')
        return redirect('home')

class VerCarritoView(LoginRequiredMixin, TemplateView):
    template_name = 'carrito.html'
    login_url = 'home'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito_repository = ServiceLocator.get_carrito_repository()
        
        carrito, _ = carrito_repository.get_or_create_for_user(self.request.user)
        prendas_en_carrito = carrito_repository.get_prendas_in_carrito(carrito)
        total = carrito_repository.calculate_total(prendas_en_carrito)
        
        context['prendas_en_carrito'] = prendas_en_carrito
        context['total'] = total
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para ver tu carrito.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class LimpiarCarritoView(View):
    @method_decorator(login_required_message)
    @method_decorator(message_decorator('success', "El carrito se ha limpiado exitosamente"))
    def get(self, request):
        carrito_repository = ServiceLocator.get_carrito_repository()
        carrito, _ = carrito_repository.get_or_create_for_user(request.user)
        carrito_repository.clear_carrito(carrito)
        return redirect('home')

