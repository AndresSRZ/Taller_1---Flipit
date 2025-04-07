from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Prenda, Carrito
from .interfaces import PrendaRepositoryInterface, CarritoRepositoryInterface, UserServiceInterface
from typing import List, Optional, Any
from django.db.models.query import QuerySet

class PrendaRepository(PrendaRepositoryInterface):
    def get_all(self) -> QuerySet:
        return Prenda.objects.all()
    
    def filter_by_nombre(self, nombre: str) -> QuerySet:
        return self.get_all().filter(nombre__icontains=nombre)
    
    def filter_by_precio(self, precio: int) -> QuerySet:
        return self.get_all().filter(precio__lte=precio)
    
    def filter_by_estado(self, estado: str) -> QuerySet:
        return self.get_all().filter(estado__icontains=estado)
    
    def filter_by_talla(self, talla: str) -> QuerySet:
        return self.get_all().filter(talla=talla)
    
    def get_by_id(self, prenda_id: int) -> Prenda:
        return Prenda.objects.get(id=prenda_id)

class CarritoRepository(CarritoRepositoryInterface):
    def get_or_create_for_user(self, user: User) -> tuple:
        return Carrito.objects.get_or_create(usuario=user)
    
    def get_prendas_in_carrito(self, carrito: Carrito) -> QuerySet:
        return carrito.prendas.all()
    
    def add_prenda_to_carrito(self, carrito: Carrito, prenda: Prenda) -> None:
        carrito.prendas.add(prenda)
    
    def clear_carrito(self, carrito: Carrito) -> None:
        carrito.prendas.clear()
    
    def calculate_total(self, prendas: List[Prenda]) -> int:
        return sum(prenda.precio for prenda in prendas)

class UserService(UserServiceInterface):
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        return authenticate(username=username, password=password)
    
    def create_user(self, username: str, email: str, password: str, 
                   first_name: str, last_name: str) -> User:
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name
        )
        user.save()
        return user
    
    def user_exists_by_username(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()
    
    def user_exists_by_email(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

