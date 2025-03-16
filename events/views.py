from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event, Category, RSVP
from events.forms import EventForm, CategoryForm, RSVPForm
from django.db.models import Count, Q
from django.utils.timezone import now
from django.contrib.auth.models import User as Participant
from django.contrib.auth.models import User
from users.forms import User_EditForm
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib import messages



# Custom error handler
def error_500(request):
    return render(request, 'error.html', status=500)

# views.py

def error(request):
    return render(request, 'error.html')

def test(request):
    return render(request, 'nav.html')

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()

def is_all_roles(user):
    return user.groups.filter(name__in=['Admin', 'Organizer', 'Participant']).exists()

@user_passes_test(is_admin_or_organizer)
@login_required
def organizer_dashboard(request):
    # Get the event type from the request, defaulting to 'all'
    type = request.GET.get('type', 'all')
    
    # Fetch all events with related category (optimized for fewer queries)
    base_events = Event.objects.select_related('category').all()
    
    # Precompute counts for events and participants
    total_participants = User.objects.count()
    total_events = base_events.count()
    today = now().date()
    date_now = base_events.filter(date__lt=now())
    
    
    # Determine the events to display based on the type
    if type == 'total_events':
        events = base_events
    elif type == 'upcoming_events':
        events = base_events.filter(date__gte=now()).order_by('date')
    elif type == 'past_events':
        events = date_now.order_by('-date')
    else:  # Default: events happening today
        events = base_events.filter(date=today).order_by('date')

    # Precompute upcoming and past event counts (avoid redundant queries)
    upcoming_events_count = base_events.filter(date__gte=now()).count()
    past_events_count = date_now.count()


    # Prepare the context for rendering
    context = {
        'events': events,
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events_count,
        'past_events': past_events_count,
        'type': type,
    }

    # Render the dashboard template with the context
    return render(request, 'organizer/organizer_dashboard.html', context)


@login_required
def home(request):
    events = Event.objects.select_related('category').prefetch_related('user_event').all()
    form = EventForm()
    location_coices = events
    
    if request.method == 'GET':
        event_name = request.GET.get('event_name', '')
        event_location = request.GET.get('event_location', '')

        if event_name and event_location:
            events = events.filter(Q(name__icontains=event_name) | Q(location=event_location))
        elif event_name:
            events = events.filter(name__icontains=event_name)
        elif event_location:
            events = events.filter(location=event_location)
    
    context = {
        'events': events.order_by('id'),
        'form': form,
        'location_choices': location_coices.distinct('location').values_list('location', flat=True)        
    }
    return render(request, 'home.html', context)

# all event related views
@user_passes_test(is_admin_or_organizer)
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)  # Log form errors
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form})


@user_passes_test(is_admin_or_organizer)
@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)  # Log form errors
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_form.html', {'form': form})


@user_passes_test(is_admin_or_organizer)
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'event/event_confirm_delete.html', {'event': event})


@login_required
@user_passes_test(is_all_roles)
def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event/event_details.html', {'event': event})

# all category related views
@user_passes_test(is_admin_or_organizer)
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})



@login_required
@user_passes_test(is_admin_or_organizer)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            print(form.errors)  # Log form errors
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_admin_or_organizer)
def category_list(request):
    categories = Category.objects.all().order_by('id')
    return render(request, 'category/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin_or_organizer)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})


# all participant related views
# def participant_create(request):
#     if request.method == 'POST':
#         form = ParticipantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('participant_list')
#     else:
#         form = ParticipantForm()
#     return render(request, 'participant/participant_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def participant_delete(request, pk):
    participant = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant/participant_confirm_delete.html', {'participant': participant})


@login_required
@user_passes_test(is_admin)
def participant_list(request):
    user = User.objects.prefetch_related('events').order_by('id').all()
    return render(request, 'participant/participant_list.html', {'participants': user})

@login_required
@user_passes_test(is_admin)
def participant_update(request, pk):
    participant = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = User_EditForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
        else:
            print(form.errors)  # Log form errors
    else:
        form = User_EditForm(instance=participant)
    return render(request, 'participant/participant_form.html', {'form': form, 'participant': participant})

# all rsvp related views
@login_required
def create_rsvp(request, event_id):
    # Get the event or return 404 if it doesn't exist
    event = get_object_or_404(Event, id=event_id)

    # Try to fetch the RSVP object if it exists
    try:
        rsvp = RSVP.objects.get(user=request.user, event=event)
    except RSVP.DoesNotExist:
        rsvp = None

    # Handle POST request
    if request.method == 'POST':
        # If RSVP exists, bind the form to the existing instance; otherwise, create a new one
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.user = request.user  # Ensure the user is set
            rsvp.event = event  # Ensure the event is set
            rsvp.save()
            messages.success(request, f"Your RSVP for '{event.name}' has been updated!")
            return redirect('home')  # Redirect to the home page (or any relevant page)
    else:
        # Prefill the form with the existing RSVP data if it exists
        form = RSVPForm(instance=rsvp)

    # Render the RSVP form template
    return render(request, 'rsvp/rsvp_form.html', {'form': form, 'event': event})

@login_required
def delete_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = get_object_or_404(RSVP, user=request.user, event=event)
    if request.method == 'POST':
        rsvp.delete()
        return redirect('participant_dashboard')
    return render(request, 'rsvp/rsvp_confirm_delete.html', {'rsvp': rsvp})

@login_required
def rsvp_list(request):
    # Get the event or return a 404 if it doesn't exist
    rsvp_list = RSVP.objects.filter(user=request.user).select_related('event').order_by('-created_at').all()
    context = {
        'user_rsvp': rsvp_list,
    }
    return render(request, 'participant/participant_dashboard.html', context)