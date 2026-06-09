from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('search_filter/', views.search_filter_task, name='search_filter_task'),
    path('clear_filters/', views.clear_filters, name='clear_filters'),
    path('logout/', views.user_logout, name='logout'),
]

