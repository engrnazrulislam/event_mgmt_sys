from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Category
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Count, Q
from events.forms import EventModelForm, ParticipantSelectionForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required


# Create your views here.
def is_Admin(user):
    return user.groups.filter(name='admin').exists()

def is_Organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_Participant(user):
    return user.groups.filter(name='Participant').exists()

def is_Admin_Organizer(user):
    return is_Admin(user) or is_Organizer(user)

def is_Admin_Participant(user):
    return is_Admin(user) or is_Participant(user)

def is_All(user):
    return is_Admin(user) or is_Organizer(user) or is_Participant(user)

def events_dashboard(request):
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
            num_participants=Count('participant',distinct=True),
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
    return render(request, 'events_dashboard.html', context)

def events_list(request):
    events = Event.objects.select_related('category').annotate(total_participants=Count('participant', distinct=True))
    context={
        "dashboard_name":"Home",
        "all_events" : events
    }
    return render(request,'events_list.html',context)

@login_required
@user_passes_test(is_All, login_url='no_permission')
def event_details(request,id):
    events = Event.objects.prefetch_related('participant').select_related('category').get(id=id)
    context={
        "event_details": events,
    }
    return render(request,'event_details.html',context)

@login_required
@user_passes_test(is_All, login_url='no_permission')
def events(request):
    all_events = Event.objects.all()
    context={
        "events":all_events
    }
    return render(request,'events.html',context)

@login_required
@user_passes_test(is_All, login_url='no_permission')
def participants(request):
    all_participants = User.objects.filter(groups__name='participant')
    return render(request, 'participants.html', {'participants': all_participants})

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def categories(request):
    all_categories = Category.objects.all()
    context={
        "categories": all_categories
    }
    return render(request,'categories.html',context)

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def create_event(request):
    event_form = EventModelForm() # For GET
    selection_form = ParticipantSelectionForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST) # For Django Model Form
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            selected_participants = selection_form.cleaned_data['participant']
            event.participants.set(selected_participants)

            messages.success(request,'Event Created Successfully')
            return redirect('create_event')
    context={
        "event_form": event_form,
        "selection_form": selection_form
    }
    return render(request,'form.html',context)

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
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

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def update_event(request, id):
    events = Event.objects.get(id=id)
    selected_participants = events.participant.all()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance = events) 
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            participants = selection_form.cleaned_data['participants']
            event.participant.set(participants)
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

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
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

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event is deleted successfully")
        
    return redirect('events')

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def delete_participant(request, id):
    if request.method == "POST":
        try:
            participant = User.objects.get(id=id)
            participant.delete()
            messages.success(request, "Participant (user) deleted successfully.")
        except User.DoesNotExist:
            messages.error(request, "Participant not found.")

    return redirect('participants')

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
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

@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = request.user

    if event.participants.filter(id=user.id).exists():
        messages.warning(request, "You already RSVPed to this event.")
    else:
        event.participants.add(user)
        messages.success(request, "RSVP successful! A confirmation email will be sent.")
    
    return redirect('event_details', id=event.id)

@login_required
@user_passes_test(is_Organizer, login_url='no_permission')
def employee_dashboard(request):
    events = request.user.rsvp_events.all()
    return render(request, 'users/employee_dashboard.html', {'events': events})

@login_required
def dashboard(request):
    if is_Admin(request.user):
        return redirect('admin_dashboard')
    elif is_Organizer(request.user):
        return redirect('manager_dashboard')
    elif is_Participant(request.user):
        return redirect('employee_dashboard')
    
    return redirect('no_permission')