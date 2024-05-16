from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.contrib import messages
from .models import Prenda, Carrito

def home(request):
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

# En views.py
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