from django.urls import path
from events import views

urlpatterns = [
     # home route
    
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('error/', views.error, name='error'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/details/', views.event_details, name='event_details'),
    
    # category
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit', views.category_update, name='category_update'),
    path('category/list', views.category_list, name='category_list'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    
    # participant
    path('participant/create/', views.participant_create, name='participant_create'),
    path('participant/<int:pk>/edit', views.participant_update, name='participant_update'),
    path('participant/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('participant/list', views.participant_list, name='participant_list'),
    
   
]

handler500 = 'events.views.error_500'
