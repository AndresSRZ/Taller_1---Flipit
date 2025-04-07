from typing import Dict, Any, Optional
from django.db.models.query import QuerySet
from .interfaces import PrendaRepositoryInterface

class PrendaFilterService:
    def __init__(self, prenda_repository: PrendaRepositoryInterface):
        self.prenda_repository = prenda_repository
    
    def apply_filters(self, filter_params: Dict[str, Any]) -> QuerySet:
        """
        Aplica todos los filtros disponibles a las prendas basado en los parámetros proporcionados.
        
        Args:
            filter_params: Diccionario con los parámetros de filtrado
            
        Returns:
            QuerySet con las prendas filtradas
        """
        # Inicializar con todas las prendas
        prendas_nombre = self.prenda_repository.get_all()
        prendas_precio = self.prenda_repository.get_all()
        prendas_estado = self.prenda_repository.get_all()
        prendas_talla = self.prenda_repository.get_all()
        
        # Aplicar filtro por nombre
        searchPrenda = filter_params.get("searchPrenda")
        if searchPrenda:
            prendas_nombre = self.prenda_repository.filter_by_nombre(searchPrenda)
        
        # Aplicar filtro por precio
        precio = filter_params.get("precio")
        if precio:
            try:
                precio = int(precio)
                prendas_precio = self.prenda_repository.filter_by_precio(precio)
            except ValueError:
                prendas_precio = self.prenda_repository.get_all().none()
        
        # Aplicar filtro por estado
        estado = filter_params.get("estado")
        if estado:
            prendas_estado = self.prenda_repository.filter_by_estado(estado)
        
        # Aplicar filtro por talla
        talla = filter_params.get("talla")
        if talla:
            prendas_talla = self.prenda_repository.filter_by_talla(talla)
        
        # Combinar todos los filtros (AND lógico)
        return prendas_nombre & prendas_precio & prendas_estado & prendas_talla

