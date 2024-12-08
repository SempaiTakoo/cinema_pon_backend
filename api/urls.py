from django.urls import path, include

from rest_framework.routers import DefaultRouter

from movies.views import (
    GenreListView, TagListView, DirectorListView, GenreViewSet, DirectorViewSet, MovieViewSet, CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register('movie', MovieViewSet)
router_v1.register('comment', CommentViewSet)
router_v1.register('genre', GenreViewSet)
router_v1.register('director', DirectorViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v2/genres/', GenreListView.as_view(), name='genre-list'),
    path('v2/tags/', TagListView.as_view(), name='tag-list'),
    path('v2/directors/', DirectorListView.as_view(), name='tag-list'),
]
