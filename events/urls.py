from django.urls import path
from events import views

urlpatterns = [
    # home route done                
    path('', views.home, name='home'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('error/', views.error, name='error'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/details/', views.event_details, name='event_details'),
    
    # category done
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit', views.category_update, name='category_update'),
    path('category/list', views.category_list, name='category_list'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    
    # participant done
    path('participant/<int:pk>/edit', views.participant_update, name='participant_update'),
    path('participant/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('participant/list', views.participant_list, name='participant_list'),


    # rsvp 
    path('rsvp/<int:event_id>/add', views.create_rsvp, name='create_rsvp'),
    path('rsvp/', views.rsvp_list, name='participant_dashboard'),
    path('rsvp/<int:event_id>/delete', views.delete_rsvp, name='delete_rsvp'),
    # path('rsvp/<int:pk>/delete', views.rsvp_delete, name='rsvp_delete'),
    
    
    
   
]
handler500 = 'events.views.error_500'
