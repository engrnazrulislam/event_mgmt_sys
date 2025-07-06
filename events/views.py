from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event, Participant, Category
from datetime import date
from django.db.models import Count


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
    context={
        "dashboard_name":"Home"
    }
    return render(request,'user_dashboard.html',context)

def event_details(request):
    context={
        "dashboard_name":"User Dashboard"
    }
    return render(request,'event_details.html',context)

def events(request):
    context={
        "dashboard_name": "Home",
    }
    return render(request,'events.html',context)

def participants(request):
    context={
        "dashboard_name": "Home",
    }
    return render(request,'participants.html',context)

def categories(request):
    context={
        "dashboard_name": "Home",
    }
    return render(request,'categories.html',context)