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

                # Eliminar todos los usuarios (⚠️ cuidado si ya hay usuarios reales en producción)
                User.objects.all().delete()

                # Crear uno nuevo
                User.objects.create_superuser(
                    username='renderadmin',
                    email='admin@render.com',
                    password='supersegura123'
                )

            except (OperationalError, ProgrammingError):
                pass


