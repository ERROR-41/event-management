from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event, Participant, Category
from events.forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponseServerError

# Custom error handler
def error_500(request):
    return render(request, 'error.html', status=500)

# views.py
def event_search(request):
    try:
        events = Event.objects.all()
        form = EventForm()

        if request.method == 'GET':
            event_name = request.GET.get('event_name', '')
            event_location = request.GET.get('event_location', '')

            if event_name:
                events = events.filter(name__icontains=event_name)
            if event_location:
                events = events.filter(location=event_location)

        # Update the choices for the location dropdown
        form.fields['event_location'].choices = [(event.location, event.location) for event in Event.objects.distinct('location')]

        return render(request, 'event_search.html', {'form': form, 'events': events})
    except Exception as e:
        print(f"Error in participant_update: {e}")
        return redirect('error')

def error(request):
    return render(request, 'error.html')

def test(request):
    return render(request, 'test.html')

def dashboard(request):
    try:
        type = request.GET.get('type', 'all')
        base_events = Event.objects.select_related('category').prefetch_related('participants').all()
        total_participants = Participant.objects.aggregate(total=Count('id'))['total']
        events = base_events  # Initialize events with base_events

        today = timezone.now().date()
        
        if type =='total_events':
            events=base_events
        elif type == 'upcoming_events':
            events = base_events.filter(date__gte=timezone.now()).order_by('date')
        elif type == 'past_events':
            events = base_events.filter(date__lt=timezone.now()).order_by('-date')
        else :
            events = base_events.filter(date=today).order_by('date')
        
        context = {
            'events': events,
            'total_events': base_events.count(),
            'categories': Category.objects.all(),
            'total_participants': total_participants,
            'upcoming_events': Event.objects.filter(date__gte=timezone.now()).order_by('date').count(),
            'past_events': Event.objects.filter(date__lt=timezone.now()).order_by('-date').count(),
            'type': type,
        }
    
        return render(request, 'dashboard.html', context)
    except Exception as e:
        return redirect('error')

def home(request):
    try:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
        form = EventForm()
        location_coices= events
        
        if request.method == 'GET':
            event_name = request.GET.get('event_name', '')
            event_location = request.GET.get('event_location', '')

            if event_name and event_location:
                events = events.filter(Q(name__icontains=event_name) | Q(location=event_location))
            elif event_name:
                events = events.filter(name__icontains=event_name)
            elif event_location:
                events = events.filter(location=event_location)
            
                
        # Populate the location choices for the form
    
        context = {
            'events': events,
            'form': form,
            'location_choices': location_coices,
            
        }
        return render(request, 'home.html', context)
    except Exception as e:
        return redirect('error')

# all event related views
def event_create(request):
    try:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = EventForm()
        return render(request, 'event_form.html', {'form': form})
    except Exception as e:
        return redirect('error')

def event_update(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = EventForm(instance=event)
        return render(request, 'event_form.html', {'form': form})
    except Exception as e:
        return redirect('error')

def event_delete(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        if request.method == 'POST':
            event.delete()
            return redirect('dashboard')
        return render(request, 'event_confirm_delete.html', {'event': event})
    except Exception as e:
        return redirect('error')

def event_details(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'event_details.html', {'event': event})
    except Exception as e:
        return redirect('error')

# all category related views
def category_create(request):
    try:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = CategoryForm()
        return render(request, 'category_form.html', {'form': form})
    except Exception as e:
        return redirect('error')

def category_update(request, pk):
    try:
        category = get_object_or_404(Category, pk=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('category_list')
        else:
            form = CategoryForm(instance=category)
        return render(request, 'category_form.html', {'form': form, 'category': category})
    except Exception as e:
        return redirect('error')
    


def category_list(request):
    try:
        categories = Category.objects.all().order_by('id')
        return render(request, 'category_list.html', {'categories': categories})
    except Exception as e:
        return redirect('error')
    
def category_delete(request, pk):
    try:
        category = get_object_or_404(Category, pk=pk)
        if request.method == 'POST':
            category.delete()
            return redirect('category_list')
        return render(request, 'category_confirm_delete.html', {'category': category})
    except Exception as e:
        return redirect('error')



# all participant related views
def participant_create(request):
    try:
        if request.method == 'POST':
            form = ParticipantForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('participant_list')
        else:
            form = ParticipantForm()
        return render(request, 'participant_form.html', {'form': form})
    except Exception as e:
        print(f"Error in participant_create: {e}")
        return redirect('error')

def participant_update(request, pk):
    try:
        participant = get_object_or_404(Participant, pk=pk)
        if request.method == 'POST':
            form = ParticipantForm(request.POST, instance=participant)
            if form.is_valid():
                form.save()
                return redirect('participant_list')
        else:
            form = ParticipantForm(instance=participant)
        return render(request, 'participant_form.html', {'form': form, 'participant': participant})
    except Exception as e:
        print(f"Error in participant_update: {e}")
        return redirect('error')

def participant_delete(request, pk):
    try:
        participant = get_object_or_404(Participant, pk=pk)
        if request.method == 'POST':
            participant.delete()
            return redirect('participant_list')
        return render(request, 'participant_confirm_delete.html', {'participant': participant})
    except Exception as e:
        return redirect('error')
    
    
def participant_list(request):
    try:
        participants = Participant.objects.all().order_by('id')
        return render(request, 'participant_list.html', {'participants': participants})
    except Exception as e:
        return redirect('error')