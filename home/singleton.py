from typing import Dict, Any, Type, TypeVar, Generic

T = TypeVar('T')

class Singleton(Generic[T]):
    """
    Implementación del patrón Singleton usando un metaclass.
    Garantiza que solo exista una instancia de cada clase que lo utilice.
    """
    _instances: Dict[Type[T], T] = {}
    
    @classmethod
    def get_instance(cls, class_: Type[T], *args, **kwargs) -> T:
        """
        Obtiene la instancia única de la clase especificada.
        Si no existe, la crea con los argumentos proporcionados.
        
        Args:
            class_: La clase de la que se quiere obtener la instancia
            *args: Argumentos posicionales para el constructor
            **kwargs: Argumentos con nombre para el constructor
            
        Returns:
            La instancia única de la clase
        """
        if class_ not in cls._instances:
            cls._instances[class_] = class_(*args, **kwargs)
        return cls._instances[class_]
    
    @classmethod
    def clear_instance(cls, class_: Type[T]) -> None:
        """
        Elimina la instancia de la clase especificada.
        Útil principalmente para pruebas.
        
        Args:
            class_: La clase cuya instancia se quiere eliminar
        """
        if class_ in cls._instances:
            del cls._instances[class_]
