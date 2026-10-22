from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='event-list'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/<int:pk>/', views.event_details, name='event-details'),
    path('events/<int:pk>/edit/', views.event_edit, name='event-edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event-delete'),
]