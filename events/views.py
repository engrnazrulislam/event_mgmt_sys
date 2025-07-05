from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event, Participant, Category

# Create your views here.
# def dashboard(request):
#     return render(request,'dashboard.html')

def dashboard(request):
    context = {
        'total_events': Event.objects.count(),
        'total_participants': Participant.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_events': Event.objects.order_by('-date')[:5],
    }
    return render(request, 'dashboard.html', context)