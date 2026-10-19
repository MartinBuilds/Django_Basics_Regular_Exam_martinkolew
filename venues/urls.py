from django.urls import path

from . import views

urlpatterns = [
    path('', views.venue_list, name='venue-list'),
    path('create/', views.venue_create, name='venue-create'),
    path('<int:pk>/', views.venue_details, name='venue-details'),
]