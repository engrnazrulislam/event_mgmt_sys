from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Category
from datetime import date
from django.db.models import Count, Q
from events.forms import EventModelForm, ParticipantSelectionForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_Admin, is_Organizer, is_Participant, is_Admin_Organizer, is_All, is_Admin_Participant
from django.views.generic import ListView
from django.views import View
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
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

#declare method decorator
event_decorator = [login_required, user_passes_test(is_All, login_url='no_permission')]
category_decorator = [login_required, user_passes_test(is_Admin_Organizer, login_url='no_permission')]
create_event_decorator = [login_required, user_passes_test(is_Admin_Organizer, login_url='no_permission')]

#class based view
@method_decorator(event_decorator, name='dispatch')
class EventDashboard(ListView):
    model = Event
    template_name = 'events_dashboard.html'
    context_object_name = 'events'

    def get_queryset(self):
        type = self.request.GET.get('type','all')
        base_query = Event.objects
        if type=='total_events':
            events_data = base_query.all()
        elif type == 'upcoming_events':
            events_data = base_query.filter(date__gt=date.today()).all()
        elif type == 'past_events':
            events_data = base_query.filter(date__lt=date.today()).all()
        elif type == 'all':
            events_data = base_query.all()
        return events_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Event.objects.all()
        counts = Event.objects.aggregate(
            num_events=Count('id',distinct=True),
            num_participants=Count('participant',distinct=True),
            )
        context['today_date']=date.today()
        context['dashboard_name'] = "Dashboard"
        context['total_events'] = counts['num_events']
        context['total_participants'] = counts['num_participants']
        context['past_events'] = data.filter(date__lt=date.today()).count()
        context['upcoming_events'] = data.filter(date__gt=date.today()).count()
        context['data'] = data
        context['events_data']= {
            "e_data":self.get_queryset,
            "d_type": type
            }
        return context

def events_list(request):
    events = Event.objects.select_related('category').annotate(total_participants=Count('participant', distinct=True))
    context={
        "dashboard_name":"Home",
        "all_events" : events
    }
    return render(request,'events_list.html',context)

#class based view
@method_decorator(event_decorator, name='dispatch')
class EventList(ListView):
    model = Event
    template_name = 'events_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_name'] = 'Home'
        events = Event.objects.select_related('category').annotate(total_participants=Count('participant', distinct=True))
        context['all_events'] = events
        return context
    
@login_required
@user_passes_test(is_All, login_url='no_permission')
def event_details(request,id):
    events = Event.objects.prefetch_related('participant').select_related('category').get(id=id)
    context={
        "event_details": events,
    }
    return render(request,'event_details.html',context)

#class based view
@method_decorator(event_decorator, name='dispatch')
class EventDetails(ListView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        context['event_details'] = Event.objects.prefetch_related('participant').select_related('category').get(id=id)
        return context



@login_required
@user_passes_test(is_All, login_url='no_permission')
def events(request):
    all_events = Event.objects.all()
    context={
        "events":all_events
    }
    return render(request,'events.html',context)

#class based view
@method_decorator(event_decorator, name='dispatch')
class Events(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Event.objects.all()
        context['events'] = all_events
        return context

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def categories(request):
    all_categories = Category.objects.all()
    context={
        "categories": all_categories
    }
    return render(request,'categories.html',context)

#class based view
@method_decorator(category_decorator, name='dispatch')
class Categories(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_categories = Category.objects.all()
        context['categories'] = all_categories
        return context

@login_required
@user_passes_test(is_Admin_Organizer, login_url='no_permission')
def create_event(request):
    event_form = EventModelForm() # For GET
    selection_form = ParticipantSelectionForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES) # For Django Model Form
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            selected_participants = selection_form.cleaned_data['participants']
            event.participant.set(selected_participants)

            messages.success(request,'Event Created Successfully')
            return redirect('create_event')
    context={
        "event_form": event_form,
        "selection_form": selection_form
    }
    return render(request,'form.html',context)

#class based view
@method_decorator(create_event_decorator, name='dispatch')
class CreateEvent(CreateView):
    model = Event
    template_name = 'form.html'
    success_url = reverse_lazy('create_event')
    form_class = EventModelForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = kwargs.get('event_form', EventModelForm) # For GET
        context['selection_form'] = kwargs.get('selection_form', ParticipantSelectionForm)
        return context
    
    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES) # For Django Model Form
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            selected_participants = selection_form.cleaned_data['participants']
            event.participant.set(selected_participants)

            messages.success(request,'Event Created Successfully')
            return redirect('create_event')
        
        context = self.get_context_data(event_form = event_form, selection_form = selection_form)
        return render(request,self.template_name, context)

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

#class based view
@method_decorator(category_decorator, name='dispatch')
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('create_category')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = kwargs.get('category_form', CategoryModelForm())
        return context
    def post(self, request, *args, **kwargs):
        category_form = CategoryModelForm(request.POST) # For Django Model Form
        if category_form.is_valid():
            """ For Django Model Form """
            category_form.save()
            
            messages.success(request,'Category Created Successfully')
            return redirect('create_category')
        
        context = self.get_context_data(category_form = category_form)
        return render(request,self.template_name,context)

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

#class based view
@method_decorator(create_event_decorator, name='dispatch')
class UpdateEvent(UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'update_form.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('update_event')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['event_form'] = kwargs.get('event_form', self.form_class(instance=event))
        context['selection_form'] = kwargs.get('selection_form', ParticipantSelectionForm(initial={
            'participants': event.participant.all()
        }))
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event_form = EventModelForm(request.POST, request.FILES, instance = event) 
        selection_form = ParticipantSelectionForm(request.POST)
        if event_form.is_valid() and selection_form.is_valid():
            """ For Django Model Form """
            event = event_form.save()
            participants = selection_form.cleaned_data['participants']
            event.participant.set(participants)
            event.save()

            messages.success(request,'Event Updated Successfully')
            return redirect('update_event',id = event.id)
        
        context = self.get_context_data(event_form = event_form, selection_form = selection_form)
        return render(request,self.template_name,context)

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
    return render(request,'update_category_form.html',context)

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
@user_passes_test(is_Organizer, login_url='no_permission')
def organizer_dashboard(request):
    # organizer_events = Event.objects.filter(created_by=request.user)
    return render(request, 'dashboard/organizer_dashboard.html')
@login_required
@user_passes_test(is_Participant, login_url='no_permission')
def participant_dashboard(request):
    return render(request, 'dashboard/participant_dashboard.html')

@login_required
def dashboard(request):
    if is_Admin(request.user):
        return redirect('admin_dashboard')
    elif is_Organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_Participant(request.user):
        return redirect('participant_dashboard')
    
    return redirect('no_permission')