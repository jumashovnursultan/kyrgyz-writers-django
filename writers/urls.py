from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('writer/<int:pk>/', views.writer_detail, name='writer_detail'),
    path('random/', views.random_writer, name='random_writer'),
    path('statistics/', views.statistics, name='statistics'),
    path('timeline/', views.timeline, name='timeline'),
    path('about/', views.about, name='about'),

    # Авторизация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Избранное
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]
