from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_index, name='search_index'),

    path('movie/', views.autocomplete_movie, name='autocomplete_movie'),
    path('movie/<str:words>/', views.search_movie, name='search_movie'),

    path('cinema/', views.autocomplete_cinema, name='autocomplete_cinema'),
    path('cinema/<str:words>/', views.search_cinema, name='search_cinema'),

]
