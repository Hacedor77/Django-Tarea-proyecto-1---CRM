from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>¡Django funciona en Render!</h1><p>Setup básico exitoso.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]
