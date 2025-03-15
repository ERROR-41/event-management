from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list

urlpatterns = [
    path('sign-up/',sign_up,name='sign_up'),
    path('sign-in/',sign_in,name='sign_in'),

    path('sign-out/',sign_out,name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate'),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('assign-role/<int:user_id>/',assign_role,name='assign_role'),
    path('create-group/',create_group,name='create_group'),
    path('group-list/',group_list,name='group_list'),
]
