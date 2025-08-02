# Al final de tu settings.py, agrega esto:

# Logging para ver errores en producción
import os


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'crm': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Si estás en producción pero necesitas ver errores detallados temporalmente
if os.environ.get('RENDER'):  # Render setea esta variable automáticamente
    DEBUG = os.environ.get('TEMP_DEBUG', 'False').lower() == 'true'