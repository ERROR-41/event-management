from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event, Participant, Category
from events.forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Count, Q
from django.utils import timezone

# Create your views here.

def error(request):
    return render(request, 'error.html')

def dashboard(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    total_participants = Participant.objects.aggregate(total=Count('id'))['total']

    context = {
        'events': events,
        'categories': Category.objects.all(),
        'total_participants': total_participants,
        'upcoming_events': Event.objects.filter(date__gte=timezone.now()).order_by('date').count(),
        'past_events': Event.objects.filter(date__lt=timezone.now()).order_by('-date').count(),
    }
    print(events)
    return render(request, 'dashboard.html', context)

# all event related views
def event_create(request):
    if request.method=='POST':
        form = EventForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboad')
    else :
        form=EventForm()
    return render(request,'event_form.html',{'form':form})  
    


        
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect(request,'event_comfirm_delete.html', {'event': event})
    
def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_details.html', {'events': event})


# all category related views

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})
        
        
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

# all participant related views

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

# def participant_update(request, pk):

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})