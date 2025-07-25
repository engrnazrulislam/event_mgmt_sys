from django.contrib import admin
from django.urls import path
from events.views import events_dashboard, events_list, event_details, events,participants,categories, create_event, create_category,update_event,delete_event, update_category, delete_category, search_result, rsvp_event  
from users.views import admin_dashboard

urlpatterns = [
path('admin/', admin.site.urls),
path('admin_dashboard/',admin_dashboard, name='admin_dashboard'),
# path('manager_dashboard/',manager_dashboard, name='manager_dashboard'),
path('events_dashboard/',events_dashboard, name='events_dashboard'),
path('event_list/',events_list,name='events_list'),
path('event_details/<int:id>',event_details,name='event_details'),
path('events/',events,name='events'),
path('participants/',participants,name='participants'),
path('categories/',categories,name='categories'),
path('create_event/',create_event,name='create_event'),
path('update_event/<int:id>',update_event,name='update_event'),
path('delete_event/<int:id>',delete_event,name='delete_event'),
# path('update_participant/<int:id>',update_participant,name='update_participant'),
# path('delete_participant/<int:id>',delete_participant,name='delete_participant'),
path('update_category/<int:id>',update_category,name='update_category'),
path('delete_category/<int:id>',delete_category,name='delete_category'),
# path('create_participant/',create_participant,name='create_participant'),
path('create_category/',create_category,name='create_category'),
path('search_result/',search_result,name='search_result'),
path('rsvp_event/<int:event_id>/', rsvp_event, name='rsvp_event')
]