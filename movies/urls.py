from django.urls import path
from .views import GenreListView,TagListView

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
]
