from django.urls import path, include

from rest_framework.routers import DefaultRouter

from movies.views import MovieViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register('movie', MovieViewSet)
router_v1.register('comment', CommentViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
