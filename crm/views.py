from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from datetime import datetime
from .models import Client, Interaction, Company
from .forms import ClientForm, InteractionForm, CompanyForm, SearchForm

@login_required
def dashboard(request):
    # Estadísticas generales
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='activo').count()
    prospects = Client.objects.filter(status='potencial').count()
    total_interactions = Interaction.objects.count()
    
    # Interacciones del mes actual
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_interactions = Interaction.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).count()
    
    # Clientes por comercial
    clients_by_user = Client.objects.values('assigned_user__username').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Últimas interacciones
    recent_interactions = Interaction.objects.select_related(
        'client', 'user'
    ).order_by('-created_at')[:5]
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'prospects': prospects,
        'total_interactions': total_interactions,
        'monthly_interactions': monthly_interactions,
        'clients_by_user': clients_by_user,
        'recent_interactions': recent_interactions,
    }
    
    return render(request, 'crm/dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class ClientListView(ListView):
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Client.objects.select_related('company', 'assigned_user')
        query = self.request.GET.get('query')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(company__name__icontains=query)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context

@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = 'crm/client_detail.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = self.object.interaction_set.all().order_by('-date')
        return context

@method_decorator(login_required, name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('client_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class InteractionListView(ListView):
    model = Interaction
    template_name = 'crm/interaction_list.html'
    context_object_name = 'interactions'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Interaction.objects.select_related('client', 'user')
        query = self.request.GET.get('query')
        
        if query:
            queryset = queryset.filter(
                Q(client__name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        
        return queryset.order_by('-date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context

@method_decorator(login_required, name='dispatch')
class InteractionCreateView(CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'crm/interaction_form.html'
    success_url = reverse_lazy('interaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Interacción creada exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class InteractionUpdateView(UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'crm/interaction_form.html'
    success_url = reverse_lazy('interaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Interacción actualizada exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class InteractionDeleteView(DeleteView):
    model = Interaction
    template_name = 'crm/interaction_confirm_delete.html'
    success_url = reverse_lazy('interaction_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Interacción eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def export_clients_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Empresa', 'Estado', 'Comercial', 'Fecha Creación'])
    
    clients = Client.objects.select_related('company', 'assigned_user')
    for client in clients:
        writer.writerow([
            client.name,
            client.email,
            client.phone,
            client.company.name,
            client.get_status_display(),
            client.assigned_user.get_full_name() or client.assigned_user.username,
            client.created_at.strftime('%Y-%m-%d')
        ])
    
    return response

@login_required
def export_interactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="interacciones.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Usuario', 'Tipo', 'Descripción', 'Fecha', 'Duración'])
    
    interactions = Interaction.objects.select_related('client', 'user')
    for interaction in interactions:
        writer.writerow([
            interaction.client.name,
            interaction.user.get_full_name() or interaction.user.username,
            interaction.get_type_display(),
            interaction.description,
            interaction.date.strftime('%Y-%m-%d'),
            interaction.duration
        ])
    
    return response