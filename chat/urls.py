from django.urls import path

from chat import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('rooms/<slug:slug>/', views.room_detail, name='room_detail'),
]
