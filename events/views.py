from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import now
from events.models import Event, Category, RSVP
from events.forms import EventForm, CategoryForm, RSVPForm
from users.forms import User_EditForm
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()


class IsAdminOrOrganizerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Admin', 'Organizer']).exists()


class IsAllRolesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Admin', 'Organizer', 'Participant']).exists()


class ErrorView(TemplateView):
    template_name = 'error.html'


class TestView(TemplateView):
    template_name = 'nav.html'


class OrganizerDashboardView(LoginRequiredMixin, IsAdminOrOrganizerMixin, TemplateView):
    template_name = 'organizer/organizer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type', 'all')
        base_events = Event.objects.select_related('category').all()
        total_participants = User.objects.count()
        total_events = base_events.count()
        today = now().date()
        date_now = base_events.filter(date__lt=now())

        if type == 'total_events':
            events = base_events
        elif type == 'upcoming_events':
            events = base_events.filter(date__gte=now()).order_by('date')
        elif type == 'past_events':
            events = date_now.order_by('-date')
        else:
            events = base_events.filter(date=today).order_by('date')

        context.update({
            'events': events,
            'total_events': total_events,
            'total_participants': total_participants,
            'upcoming_events': base_events.filter(date__gte=now()).count(),
            'past_events': date_now.count(),
            'type': type,
        })
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.select_related('category').prefetch_related('user_event').all()
        form = EventForm()
        event_name = self.request.GET.get('event_name', '')
        event_location = self.request.GET.get('event_location', '')

        if event_name and event_location:
            events = events.filter(Q(name__icontains=event_name) | Q(location=event_location))
        elif event_name:
            events = events.filter(name__icontains=event_name)
        elif event_location:
            events = events.filter(location=event_location)

        context.update({
            'events': events.order_by('id'),
            'form': form,
            'location_choices': events.distinct('location').values_list('location', flat=True),
        })
        return context


class EventCreateView(LoginRequiredMixin, IsAdminOrOrganizerMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)


class EventUpdateView(LoginRequiredMixin, IsAdminOrOrganizerMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('home')


class EventDeleteView(LoginRequiredMixin, IsAdminOrOrganizerMixin, DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('home')


class EventDetailView(LoginRequiredMixin, IsAllRolesMixin, DetailView):
    model = Event
    template_name = 'event/event_details.html'


class CategoryCreateView(LoginRequiredMixin, IsAdminOrOrganizerMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, IsAdminOrOrganizerMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryListView(LoginRequiredMixin, IsAdminOrOrganizerMixin, ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    ordering = ['id']


class CategoryDeleteView(LoginRequiredMixin, IsAdminOrOrganizerMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


class ParticipantListView(LoginRequiredMixin, IsAdminMixin, ListView):
    model = User
    template_name = 'participant/participant_list.html'
    context_object_name = 'participants'
    ordering = ['id']


class ParticipantUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = User
    form_class = User_EditForm
    template_name = 'participant/participant_form.html'
    success_url = reverse_lazy('participant_list')


class ParticipantDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = User
    template_name = 'participant/participant_confirm_delete.html'
    success_url = reverse_lazy('participant_list')


class RSVPCreateView(LoginRequiredMixin, CreateView):
    model = RSVP
    form_class = RSVPForm
    template_name = 'rsvp/rsvp_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = get_object_or_404(Event, id=self.kwargs['event_id'])
        messages.success(self.request, f"Your RSVP for '{form.instance.event.name}' has been updated!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class RSVPDeleteView(LoginRequiredMixin, DeleteView):
    model = RSVP
    template_name = 'rsvp/rsvp_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(RSVP, user=self.request.user, event_id=self.kwargs['event_id'])

    def get_success_url(self):
        return reverse_lazy('participant_dashboard')


class RSVPListView(LoginRequiredMixin, ListView):
    model = RSVP
    template_name = 'participant/participant_dashboard.html'
    context_object_name = 'user_rsvp'

    def get_queryset(self):
        return RSVP.objects.filter(user=self.request.user).select_related('event').order_by('-created_at')
