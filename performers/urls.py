from django.urls import path

from . import views

urlpatterns = [
    path('', views.performer_list, name='performer-list'),
    path('create/', views.performer_create, name='performer-create'),
    path('<int:pk>/', views.performer_details, name='performer-details'),
    path('<int:pk>/edit/', views.performer_edit, name='performer-edit'),
    path('<int:pk>/delete/', views.performer_delete, name='performer-delete'),
]