from abc import ABC, abstractmethod
from typing import List, Optional, Any
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

class PrendaRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet:
        pass
    
    @abstractmethod
    def filter_by_nombre(self, nombre: str) -> QuerySet:
        pass
    
    @abstractmethod
    def filter_by_precio(self, precio: int) -> QuerySet:
        pass
    
    @abstractmethod
    def filter_by_estado(self, estado: str) -> QuerySet:
        pass
    
    @abstractmethod
    def filter_by_talla(self, talla: str) -> QuerySet:
        pass
    
    @abstractmethod
    def get_by_id(self, prenda_id: int) -> Any:
        pass

class CarritoRepositoryInterface(ABC):
    @abstractmethod
    def get_or_create_for_user(self, user: User) -> tuple:
        pass
    
    @abstractmethod
    def get_prendas_in_carrito(self, carrito: Any) -> QuerySet:
        pass
    
    @abstractmethod
    def add_prenda_to_carrito(self, carrito: Any, prenda: Any) -> None:
        pass
    
    @abstractmethod
    def clear_carrito(self, carrito: Any) -> None:
        pass
    
    @abstractmethod
    def calculate_total(self, prendas: List[Any]) -> int:
        pass

class UserServiceInterface(ABC):
    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def create_user(self, username: str, email: str, password: str, 
                   first_name: str, last_name: str) -> User:
        pass
    
    @abstractmethod
    def user_exists_by_username(self, username: str) -> bool:
        pass
    
    @abstractmethod
    def user_exists_by_email(self, email: str) -> bool:
        pass

