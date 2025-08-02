#from django.apps import AppConfig


#class CrmConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    #name = 'crm'


import os
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

    def ready(self):
        if os.environ.get("RENDER") == "true":
            try:
                User = get_user_model()
                if not User.objects.filter(username='renderadmin').exists():
                    print("Creando superusuario renderadmin...")
                    User.objects.create_superuser(
                        username='renderadmin',
                        email='admin@render.com',
                        password='supersegura123'
                    )
                    print("Superusuario creado.")
            except (OperationalError, ProgrammingError) as e:
                print(f"Error en ready(): {e}")



