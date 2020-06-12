from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'', views.RatingViewSet, basename="rating")


urlpatterns = [
    path('map/', views.get_cinema_width, name='get_cinema_width'),
    path('map/<int:cinema_id>/movie/', views.get_fast_movie, name='get_fast_movie'),

    path('<int:cinema_id>/', views.cinema_detail, name='cinema_detail'),
    path('<int:cinema_id>/pick/', views.pick_cinema, name='pick_cinema'),
    path('<int:cinema_id>/score/', views.get_cinema_rating_avg, name='get_cinema_rating_avg'),

    path('rating/', views.create_cinema_rating, name='create_cinema_rating'),
    path('rating/<int:rating_id>/', views.patch_delete_cinema_rating, name='patch_delete_cinema_rating'),
    path('rating/page/', include(router.urls)),
]
