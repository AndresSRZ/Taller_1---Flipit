from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Prenda(models.Model):
    imagen = models.ImageField(upload_to='img/')
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    estado = models.CharField(max_length=200)
    talla = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

# En models.py
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    prendas = models.ManyToManyField(Prenda)