from django.db import router
from django.urls import path, re_path, include

from rest_framework import routers

from movies.views import (
    MovieViewSet,
    CommentViewSet,
    GenreViewSet,
    DirectorViewSet,
    MovieRecommendationsViewSet,
    RatingViewSet,
    TagViewSet,
    UserRecommendationsViewSet
)
from users.views import UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('movies', MovieViewSet)
router_v1.register('users', UserViewSet)
router_v1.register('comments', CommentViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('ratings', RatingViewSet)
router_v1.register('directors', DirectorViewSet)
router_v1.register('movie_recommendations', MovieRecommendationsViewSet)
router_v1.register('user_recommendations', UserRecommendationsViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
