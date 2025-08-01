from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # URLs de clientes
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('clients/export/', views.export_clients_csv, name='export_clients'),
    
    # URLs de interacciones
    path('interactions/', views.InteractionListView.as_view(), name='interaction_list'),
    path('interactions/create/', views.InteractionCreateView.as_view(), name='interaction_create'),
    path('interactions/<int:pk>/edit/', views.InteractionUpdateView.as_view(), name='interaction_update'),
    path('interactions/<int:pk>/delete/', views.InteractionDeleteView.as_view(), name='interaction_delete'),
    path('interactions/export/', views.export_interactions_csv, name='export_interactions'),
]