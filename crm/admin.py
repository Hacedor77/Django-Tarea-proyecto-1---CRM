from django.contrib import admin
from .models import Client, Interaction, Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'created_at']
    search_fields = ['name', 'sector']
    list_filter = ['sector', 'created_at']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'status', 'assigned_user', 'created_at']
    list_filter = ['status', 'company', 'assigned_user', 'created_at']
    search_fields = ['name', 'email', 'company__name']
    date_hierarchy = 'created_at'

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['client', 'user', 'type', 'date', 'duration']
    list_filter = ['type', 'date', 'user']
    search_fields = ['client__name', 'description']
    date_hierarchy = 'date'