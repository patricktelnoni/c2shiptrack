# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_form, name='index'),
    path('login', views.process_login, name='login_via_api'),
    path('create_staff', views.process_user, name='create_staff_via_api'),
    path('create_lokasi', views.process_lokasi, name='create_lokasi_via_api'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('lokasi_form', views.lokasi_form, name='form_lokasi'),
    path('lokasi_list', views.list_lokasi, name='list_lokasi'),
    path('user_form', views.user_form, name='form_user'),
    path('list_user', views.list_user, name='list_user'),
    path('list_session', views.list_session, name='list_session'),
    path('logout', views.logout_view, name='logout'),
    # path('<str:room_name>/', views.room, name='room'),

]