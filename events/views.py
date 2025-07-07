from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Participant, Category
from datetime import date
from django.db.models import Count, Q
from events.forms import EventModelForm
from django.contrib import messages


# Create your views here.
# def dashboard(request):
#     return render(request,'dashboard.html')

def dashboard(request):
    type=request.GET.get('type','all')
    base_query = Event.objects
    if type=='total_events':
        events_data = base_query.all()
    elif type == 'upcoming_events':
        events_data = base_query.filter(date__gt=date.today()).all()
    elif type == 'past_events':
        events_data = base_query.filter(date__lt=date.today()).all()
    elif type == 'all':
        events_data = base_query.all()
    
    # by default Data
    data= base_query.all()

    counts = Event.objects.aggregate(
            num_events=Count('id',distinct=True),
            num_participants=Count('participants',distinct=True),
            )
    today_date=date.today()
    context = {
        'dashboard_name':"Dashboard",
        'total_events': counts['num_events'],
        'total_participants': counts['num_participants'],
        'past_events':data.filter(date__lt=date.today()).count(),
        'upcoming_events': data.filter(date__gt=date.today()).count(),
        'data':data,
        'today_date':today_date,
        'events_data':{
            "e_data":events_data,
            "d_type": type
            },
    }
    return render(request, 'dashboard.html', context)

def user_dashboard(request):
    events = Event.objects.select_related('category').annotate(total_participants=Count('participants', distinct=True))
    context={
        "dashboard_name":"Home",
        "all_events" : events
    }
    return render(request,'user_dashboard.html',context)

def event_details(request,id):
    events = Event.objects.prefetch_related('participants').select_related('category').get(id=id)
    context={
        "dashboard_name":"User Dashboard",
        "event_details": events,
    }
    return render(request,'event_details.html',context)

def events(request):
    all_events = Event.objects.all()
    context={
        "dashboard_name": "Home",
        "events":all_events
    }
    return render(request,'events.html',context)

def participants(request):
    all_participants = Participant.objects.all()
    context={
        "dashboard_name": "Home",
        "participants": all_participants
    }
    return render(request,'participants.html',context)

def categories(request):
    all_categories = Category.objects.all()
    context={
        "dashboard_name": "Home",
        "categories": all_categories
    }
    return render(request,'categories.html',context)

def create_event(request):
    events=Event.objects.all()
    event_form = EventModelForm() # For GET

    if request.method == 'POST':
        event_form = EventModelForm(request.POST) # For Django Model Form
        if event_form.is_valid():
            """ For Django Model Form """
            event_form.save()
            messages.success(request,'Event Created Successfully')
            return redirect('create-event')
    context={
        "dashboard_name": 'Home',
        "event_form": event_form,
    }
    return render(request,'form.html',context)