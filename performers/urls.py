from django.urls import path

from . import views

urlpatterns = [
    path('', views.performer_list, name='performer-list'),
]