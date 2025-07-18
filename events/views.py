from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Participant, Category
from datetime import date
from django.db.models import Count, Q
from events.forms import EventModelForm, ParticipantSelectionForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages


# Create your views here.
# def dashboard(request):
#     return render(request,'dashboard.html')

def events_overview(request):
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
    return render(request, 'events_overview.html', context)

def events_list(request):
    events = Event.objects.select_related('category').annotate(total_participants=Count('participants', distinct=True))
    context={
        "dashboard_name":"Home",
        "all_events" : events
    }
    return render(request,'events_list.html',context)

def event_details(request,id):
    events = Event.objects.prefetch_related('participants').select_related('category').get(id=id)
    context={
        "event_details": events,
    }
    return render(request,'event_details.html',context)

def events(request):
    all_events = Event.objects.all()
    context={
        "events":all_events
    }
    return render(request,'events.html',context)

def participants(request):
    all_participants = Participant.objects.all()
    context={
        "participants": all_participants
    }
    return render(request,'participants.html',context)

def categories(request):
    all_categories = Category.objects.all()
    context={
        "categories": all_categories
    }
    return render(request,'categories.html',context)

def create_event(request):
    event_form = EventModelForm() # For GET
    selection_form = ParticipantSelectionForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST) # For Django Model Form
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            selected_participants = selection_form.cleaned_data['participants']
            for participant in selected_participants:
                participant.participant_to.add(event)

            messages.success(request,'Event Created Successfully')
            return redirect('create_event')
    context={
        "event_form": event_form,
        "selection_form": selection_form
    }
    return render(request,'form.html',context)

def create_participant(request):
    participant_form = ParticipantModelForm() # For GET

    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST) # For Django Model Form
        if participant_form.is_valid():
            """ For Django Model Form """
            participant_form.save()
            
            messages.success(request,'Participant Created Successfully')
            return redirect('create_participant')
    context={
        "participant_form": participant_form
    }
    return render(request,'participant_form.html',context)

def create_category(request):
    category_form = CategoryModelForm() # For GET

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST) # For Django Model Form
        if category_form.is_valid():
            """ For Django Model Form """
            category_form.save()
            
            messages.success(request,'Category Created Successfully')
            return redirect('create_category')
    context={
        "category_form": category_form
    }
    return render(request,'category_form.html',context)

def update_event(request, id):
    events = Event.objects.get(id=id)
    selected_participants = events.participants.all()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance = events) 
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            participants = selection_form.cleaned_data['participants']
            event.participants.set(participants)
            event.save()

            messages.success(request,'Event Updated Successfully')
            return redirect('update_event',id=id)
    else:
        event_form = EventModelForm(instance=events)
        selection_form = ParticipantSelectionForm(
            initial={'participants': selected_participants}
        )
    context={
        "event_form": event_form,
        "selection_form": selection_form
    }
    return render(request,'form.html',context)

def update_participant(request, id):
    participants = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance = participants) # For GET

    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST, instance = participants) # For Django Model Form
        if participant_form.is_valid():
            """ For Django Model Form """
            participant_form.save()
            
            messages.success(request,'Participant Updated Successfully')
            return redirect('update_participant',id=id)
    context={
        "participant_form": participant_form
    }
    return render(request,'participant_form.html',context)

def update_category(request, id):
    categories = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance = categories) # For GET

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance = categories) # For Django Model Form
        if category_form.is_valid():
            """ For Django Model Form """
            category_form.save()
            
            messages.success(request,'Category Updated Successfully')
            return redirect('update_category', id=id)
    context={
        "category_form": category_form
    }
    return render(request,'category_form.html',context)

def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event is deleted successfully")
        
    return redirect('events')
    
def delete_participant(request, id):
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request,"Participant is deleted successfully")
        
    return redirect('participants')

def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request,"Category is deleted successfully")
        
    return redirect('categories')

def search_result(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Event.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    return render(request, 'search_result.html', {
        'results': results,
        'query': query,
    })