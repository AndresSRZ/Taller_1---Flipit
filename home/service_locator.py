from .singleton import Singleton
from .interfaces import PrendaRepositoryInterface, CarritoRepositoryInterface, UserServiceInterface
from .repositories import PrendaRepository, CarritoRepository, UserService
from .services import PrendaFilterService
from typing import Dict, Any, Type

class ServiceLocator:
    """
    Implementación del patrón Service Locator que utiliza Singleton.
    Proporciona un punto centralizado para obtener servicios y repositorios.
    """
    
    @staticmethod
    def get_prenda_repository() -> PrendaRepositoryInterface:
        """
        Obtiene la instancia única del repositorio de prendas.
        
        Returns:
            La instancia del repositorio de prendas
        """
        return Singleton.get_instance(PrendaRepository)
    
    @staticmethod
    def get_carrito_repository() -> CarritoRepositoryInterface:
        """
        Obtiene la instancia única del repositorio de carritos.
        
        Returns:
            La instancia del repositorio de carritos
        """
        return Singleton.get_instance(CarritoRepository)
    
    @staticmethod
    def get_user_service() -> UserServiceInterface:
        """
        Obtiene la instancia única del servicio de usuarios.
        
        Returns:
            La instancia del servicio de usuarios
        """
        return Singleton.get_instance(UserService)
    
    @staticmethod
    def get_prenda_filter_service() -> PrendaFilterService:
        """
        Obtiene la instancia única del servicio de filtrado de prendas.
        Nota: Este método asegura que el repositorio de prendas también sea un singleton.
        
        Returns:
            La instancia del servicio de filtrado de prendas
        """
        prenda_repository = ServiceLocator.get_prenda_repository()
        return Singleton.get_instance(PrendaFilterService, prenda_repository)
