from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('',include('core.urls')),
    path('events/',include('events.urls'))#adding urls of the events app
] + debug_toolbar_urls()
