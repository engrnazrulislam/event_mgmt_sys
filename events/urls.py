from django.contrib import admin
from django.urls import path
from events.views import dashboard, user_dashboard, event_details, events,participants,categories

urlpatterns = [
path('admin/', admin.site.urls),
path('dashboard/',dashboard, name='dashboard'),
path('user_dashboard/',user_dashboard,name='user_dashboard'),
path('event_details/',event_details,name='event_details'),
path('events/',events,name='events'),
path('participants/',participants,name='participants'),
path('categories/',categories,name='categories')
]