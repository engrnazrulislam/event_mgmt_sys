from django.contrib import admin
from django.urls import path,include
from events.views import user_dashboard
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_dashboard,name='user_dashboard'),
    path('users/', include('users.urls')),
    path('events/',include('events.urls')), #adding urls of the events app
]+ debug_toolbar_urls()
