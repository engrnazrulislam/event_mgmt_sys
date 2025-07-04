from django.contrib import admin
from django.urls import path
from events.views import dashboard

urlpatterns = [
path('admin/', admin.site.urls),
path('dashboard/',dashboard, name='dashboard')
]