from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.core.management import call_command
from django.apps import apps
import os

class Command(BaseCommand):
    help = 'Setup completo para producción'
    
    def handle(self, *args, **options):
        try:
            # 1. Aplicar migraciones estándar de Django
            self.stdout.write("Aplicando migraciones...")
            call_command('migrate', verbosity=0)
            self.stdout.write("✓ Migraciones aplicadas")
            
            # 2. Crear superusuario
            self.create_admin_user()
            
            # 3. Crear datos de ejemplo solo si tenemos los modelos
            if self.models_exist():
                self.create_sample_data()
            
            self.stdout.write(
                self.style.SUCCESS('🎉 ¡Setup de producción completado!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error en setup: {str(e)}')
            )
            # No hacer raise para que no falle el deploy
            return
    
    def models_exist(self):
        """Verificar si los modelos CRM existen"""
        try:
            from crm.models import Company, Client, Interaction
            return True
        except:
            return False
    def create_sample_data(self):
        """Crear datos de ejemplo usando los modelos Django"""
        try:
            from crm.models import Company, Client, Interaction
            from datetime import datetime, date, timedelta
            import random
            
            # Crear usuarios comerciales
            user1, created = User.objects.get_or_create(
                username='ana_comercial',
                defaults={
                    'first_name': 'Ana',
                    'last_name': 'Comercial',
                    'email': 'ana@empresa.com',
                    'is_staff': True
                }
            )
            if created:
                user1.set_password('comercial123')
                user1.save()
                self.stdout.write("✓ Usuario Ana creado")
            
            user2, created = User.objects.get_or_create(
                username='pedro_vendedor',
                defaults={
                    'first_name': 'Pedro',
                    'last_name': 'Vendedor', 
                    'email': 'pedro@empresa.com',
                    'is_staff': True
                }
            )
            if created:
                user2.set_password('vendedor123')
                user2.save()
                self.stdout.write("✓ Usuario Pedro creado")
            
            # Crear empresas
            companies_data = [
                {'name': 'Tech Solutions SL', 'sector': 'Tecnología'},
                {'name': 'Innovate Corp', 'sector': 'Consultoría'},
                {'name': 'StartUp Digital', 'sector': 'Software'},
            ]
            
            companies = []
            for comp_data in companies_data:
                company, created = Company.objects.get_or_create(**comp_data)
                companies.append(company)
                if created:
                    self.stdout.write(f"✓ Empresa {company.name} creada")
            
            # Crear clientes
            clients_data = [
                {
                    'name': 'Juan Pérez', 
                    'email': 'juan.perez@techsolutions.com',
                    'phone': '+34 666 123 456', 
                    'status': 'activo',
                    'assigned_user': user1
                },
                {
                    'name': 'María García',
                    'email': 'maria.garcia@innovate.es', 
                    'phone': '+34 677 234 567',
                    'status': 'potencial', 
                    'assigned_user': user2
                },
            ]
            
            for i, client_data in enumerate(clients_data):
                client_data['company'] = companies[i % len(companies)]
                client, created = Client.objects.get_or_create(
                    email=client_data['email'],
                    defaults=client_data
                )
                if created:
                    self.stdout.write(f"✓ Cliente {client.name} creado")
            
            self.stdout.write("✓ Datos de ejemplo creados")
            
        except Exception as e:
            self.stdout.write(f"⚠ Error creando datos de ejemplo: {e}")
            # No fallar por esto