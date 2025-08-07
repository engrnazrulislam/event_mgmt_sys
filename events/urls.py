from django.contrib import admin
from django.urls import path
from events.views import events_dashboard, events_list ,event_details, events,categories, create_event, create_category,update_event,delete_event, update_category, delete_category, search_result, organizer_dashboard, participant_dashboard, dashboard
from events.views import EventDashboard, EventList, EventDetails, Events, Categories, CreateEvent, CreateCategory, UpdateEvent
from users.views import admin_dashboard

urlpatterns = [
path('admin/', admin.site.urls),
path('admin_dashboard/',admin_dashboard, name='admin_dashboard'),
path('organizer_dashboard/',organizer_dashboard, name='organizer_dashboard'),
path('participant_dashboard/',participant_dashboard, name='participant_dashboard'),
# path('events_dashboard/',events_dashboard, name='events_dashboard'),
path('events_dashboard/',EventDashboard.as_view(), name='events_dashboard'),
path('event_list/',EventList.as_view(),name='events_list'),
# path('event_details/<int:id>',event_details,name='event_details'),
path('event_details/<int:id>',EventDetails.as_view(),name='event_details'),
# path('events/',events,name='events'),
path('events/',Events.as_view(),name='events'),
# path('categories/',categories,name='categories'),
path('categories/',Categories.as_view(),name='categories'),
# path('create_event/',create_event,name='create_event'),
path('create_event/',CreateEvent.as_view(),name='create_event'),
# path('update_event/<int:id>',update_event,name='update_event'),
path('update_event/<int:id>',UpdateEvent.as_view(),name='update_event'),
path('delete_event/<int:id>',delete_event,name='delete_event'),

path('update_category/<int:id>',update_category,name='update_category'),
path('delete_category/<int:id>',delete_category,name='delete_category'),

# path('create_category/',create_category,name='create_category'),
path('create_category/',CreateCategory.as_view(),name='create_category'),
path('search_result/',search_result,name='search_result'),
path('dashboard/',dashboard, name='dashboard')
]