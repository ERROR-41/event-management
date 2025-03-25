from django.urls import path
from events import views

urlpatterns = [
    # home route done
    path("", views.HomeView.as_view(), name="home"),
    path(
        "dashboard/", views.OrganizerDashboardView.as_view(), name="organizer_dashboard"
    ),
    path("error/", views.ErrorView.as_view(), name="error"),
    path("events/create/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit", views.EventUpdateView.as_view(), name="event_update"),
    path(
        "events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"
    ),
    path(
        "events/<int:pk>/details/",
        views.EventDetailView.as_view(),
        name="event_details",
    ),
    # category done
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/<int:pk>/edit",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path("category/list", views.CategoryListView.as_view(), name="category_list"),
    path(
        "category/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    # participant done
    path(
        "participant/<int:pk>/edit",
        views.ParticipantUpdateView.as_view(),
        name="participant_update",
    ),
    path(
        "participant/<int:pk>/delete/",
        views.ParticipantDeleteView.as_view(),
        name="participant_delete",
    ),
    path(
        "participant/list", views.ParticipantListView.as_view(), name="participant_list"
    ),
    # rsvp
    path("rsvp/<int:event_id>/add", views.RSVPCreateView.as_view(), name="create_rsvp"),
    path("rsvp/", views.RSVPListView.as_view(), name="participant_dashboard"),
    path(
        "rsvp/<int:event_id>/delete", views.RSVPDeleteView.as_view(), name="delete_rsvp"
    ),
    # path('rsvp/<int:pk>/delete', views.rsvp_delete, name='rsvp_delete'),
]
handler500 = 'events.views.error_500'
