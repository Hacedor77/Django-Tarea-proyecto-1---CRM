from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def status_badge(status):
    """Convierte el estado del cliente en un badge HTML"""
    badges = {
        'activo': '<span class="badge bg-success">Activo</span>',
        'potencial': '<span class="badge bg-warning text-dark">Potencial</span>', # Añadido text-dark para mejor contraste
        'inactivo': '<span class="badge bg-secondary">Inactivo</span>',
    }
    return mark_safe(badges.get(status, status))

@register.filter
def interaction_icon(interaction_type):
    """Devuelve un icono FontAwesome según el tipo de interacción"""
    icons = {
        'llamada': 'fas fa-phone',
        'email': 'fas fa-envelope',
        'reunion': 'fas fa-users',
        'visita': 'fas fa-map-marker-alt',
    }
    return icons.get(interaction_type, 'fas fa-comment')