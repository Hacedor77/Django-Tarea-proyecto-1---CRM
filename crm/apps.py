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
        # Solo ejecutar en Render.com (si defines la variable de entorno)
        if os.environ.get("RENDER") == "true":
            try:
                User = get_user_model()
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(
                        username='admin',
                        password='admin123'
                    )
            except (OperationalError, ProgrammingError):
                # Puede fallar si la base de datos aún no está lista
                pass

