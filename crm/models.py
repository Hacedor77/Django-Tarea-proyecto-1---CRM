from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    sector = models.CharField(max_length=100, verbose_name="Sector")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    
    def __str__(self):
        return self.name

class Client(models.Model):
    STATUS_CHOICES = [
        ('potencial', 'Potencial'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Empresa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='potencial', verbose_name="Estado")
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Comercial asignado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"
    
    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'pk': self.pk})

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunión'),
        ('visita', 'Visita'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    date = models.DateField(verbose_name="Fecha")
    duration = models.IntegerField(default=0, help_text="Duración en minutos", verbose_name="Duración")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.type} - {self.client.name} ({self.date})"