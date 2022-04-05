from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('group/<slug:gn>/', views.group_posts),
]
