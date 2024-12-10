from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from movies.views import (
    GenreListView, TagListView, GenreViewSet, MovieViewSet, CommentViewSet
)
from users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('movie', MovieViewSet)
router_v1.register('comment', CommentViewSet)
router_v1.register('genre', GenreViewSet)
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('v2/genres/', GenreListView.as_view(), name='genre-list'),
    path('v2/tags/', TagListView.as_view(), name='tag-list'),

]
