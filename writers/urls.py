from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('writer/<int:pk>/', views.writer_detail, name='writer_detail'),
    path('random/', views.random_writer, name='random_writer'),
    path('statistics/', views.statistics, name='statistics'),
    path('timeline/', views.timeline, name='timeline'),
path('about/', views.about, name='about'),


]