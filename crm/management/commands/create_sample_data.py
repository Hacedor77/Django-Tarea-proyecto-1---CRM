from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import Company, Client, Interaction
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el CRM'
    
    def handle(self, *args, **options):
        # Crear usuarios comerciales
        user1, created = User.objects.get_or_create(
            username='ana_comercial',
            defaults={
                'first_name': 'Ana',
                'last_name': 'Comercial',
                'email': 'ana@empresa.com'
            }
        )
        
        user2, created = User.objects.get_or_create(
            username='pedro_vendedor',
            defaults={
                'first_name': 'Pedro',
                'last_name': 'Vendedor',
                'email': 'pedro@empresa.com'
            }
        )
        
        # Crear empresas
        companies_data = [
            {'name': 'Tech Solutions SL', 'sector': 'Tecnología'},
            {'name': 'Innovate Corp', 'sector': 'Consultoría'},
            {'name': 'StartUp Digital', 'sector': 'Software'},
            {'name': 'Marketing Pro', 'sector': 'Marketing'},
            {'name': 'Finance Plus', 'sector': 'Finanzas'},
        ]
        
        companies = []
        for comp_data in companies_data:
            company, created = Company.objects.get_or_create(**comp_data)
            companies.append(company)
        
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
            {
                'name': 'Carlos López',
                'email': 'carlos@startup.io',
                'phone': '+34 688 345 678',
                'status': 'inactivo',
                'assigned_user': user1
            },
        ]
        
        clients = []
        for i, client_data in enumerate(clients_data):
            client_data['company'] = companies[i % len(companies)]
            client, created = Client.objects.get_or_create(
                email=client_data['email'],
                defaults=client_data
            )
            clients.append(client)
        
        # Crear interacciones
        interaction_types = ['llamada', 'email', 'reunion', 'visita']
        descriptions = [
            'Primera llamada comercial. Cliente interesado.',
            'Envío de propuesta comercial.',
            'Reunión de seguimiento.',
            'Demostración del producto.',
            'Negociación de contrato.',
            'Cierre de venta exitoso.',
        ]
        
        for client in clients:
            for i in range(random.randint(1, 4)):
                Interaction.objects.get_or_create(
                    client=client,
                    user=random.choice([user1, user2]),
                    type=random.choice(interaction_types),
                    description=random.choice(descriptions),
                    date=date.today() - timedelta(days=random.randint(1, 30)),
                    duration=random.randint(15, 120)
                )