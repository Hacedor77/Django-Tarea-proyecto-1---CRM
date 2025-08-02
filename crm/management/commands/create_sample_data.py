from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import Company, Client, Interaction
from datetime import date, timedelta
import random
import os

class Command(BaseCommand):
    help = 'Crea superusuario y datos de ejemplo para el CRM'
    
    def handle(self, *args, **options):
        # CREAR SUPERUSUARIO PRIMERO
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Superusuario "{admin_username}" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ Superusuario "{admin_username}" ya existe')
            )
        
        # CREAR USUARIOS COMERCIALES
        user1, created = User.objects.get_or_create(
            username='ana_comercial',
            defaults={
                'first_name': 'Ana',
                'last_name': 'Comercial',
                'email': 'ana@empresa.com',
                'is_staff': True  # Para que puedan acceder al admin
            }
        )
        if created:
            user1.set_password('comercial123')  # Establecer contraseña
            user1.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario Ana Comercial creado'))
        
        user2, created = User.objects.get_or_create(
            username='pedro_vendedor',
            defaults={
                'first_name': 'Pedro',
                'last_name': 'Vendedor',
                'email': 'pedro@empresa.com',
                'is_staff': True  # Para que puedan acceder al admin
            }
        )
        if created:
            user2.set_password('vendedor123')  # Establecer contraseña
            user2.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario Pedro Vendedor creado'))
        
        # CREAR EMPRESAS
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
            if created:
                self.stdout.write(f'✓ Empresa {company.name} creada')
        
        # CREAR CLIENTES
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
            if created:
                self.stdout.write(f'✓ Cliente {client.name} creado')
        
        # CREAR INTERACCIONES
        interaction_types = ['llamada', 'email', 'reunion', 'visita']
        descriptions = [
            'Primera llamada comercial. Cliente interesado.',
            'Envío de propuesta comercial.',
            'Reunión de seguimiento.',
            'Demostración del producto.',
            'Negociación de contrato.',
            'Cierre de venta exitoso.',
        ]
        
        interactions_created = 0
        for client in clients:
            for i in range(random.randint(1, 4)):
                interaction, created = Interaction.objects.get_or_create(
                    client=client,
                    user=random.choice([user1, user2]),
                    type=random.choice(interaction_types),
                    description=random.choice(descriptions),
                    date=date.today() - timedelta(days=random.randint(1, 30)),
                    defaults={'duration': random.randint(15, 120)}
                )
                if created:
                    interactions_created += 1
        
        self.stdout.write(f'✓ {interactions_created} interacciones creadas')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 ¡Setup completado exitosamente!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'👤 Admin: {admin_username} / {admin_password}')
        )
        self.stdout.write(
            self.style.SUCCESS('👥 Usuarios comerciales: ana_comercial y pedro_vendedor (contraseña: comercial123 y vendedor123)')
        )