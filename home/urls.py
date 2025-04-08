from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('process_registration/', views.ProcessRegistrationView.as_view(), name='process_registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('agregar_al_carrito/<int:prenda_id>/', views.AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('ver_carrito/', views.VerCarritoView.as_view(), name='ver_carrito'),
    path('limpiar_carrito/', views.LimpiarCarritoView.as_view(), name='limpiar_carrito'),
]