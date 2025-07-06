from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event, Participant, Category

# Create your views here.
# def dashboard(request):
#     return render(request,'dashboard.html')

def dashboard(request):
    context = {
        'dashboard_name':"Dashboard",
        'total_events': Event.objects.count(),
        'total_participants': Participant.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_events': Event.objects.order_by('-date')[:5].count(),
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