from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'', views.RatingViewSet, basename="rating")


urlpatterns = [
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/pick/', views.pick_movie, name='pick_movie'),
    path('<int:movie_id>/onscreen/', views.get_onscreen_cinema, name='get_onscreen_cinema'),
    path('<int:movie_id>/score/', views.get_rating_avg, name='get_rating_avg'),

    path('rating/', views.create_rating, name='create_rating'),
    path('rating/page/', include(router.urls)),
    path('rating/<int:rating_id>/', views.patch_delete_rating, name='path_delete_rating'),
]
