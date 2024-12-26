from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, re_path, include

from rest_framework import routers, permissions

from movies.views import (
    MovieViewSet,
    CommentViewSet,
    GenreViewSet,
    DirectorViewSet
)
from users.views import UserViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='1.1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router_v1 = routers.DefaultRouter()
router_v1.register('movies', MovieViewSet)
router_v1.register('users', UserViewSet)
router_v1.register('comments', CommentViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('directors', DirectorViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),

    path(
        'spectacular/schema/',
        SpectacularAPIView.as_view(),
        name='spectacular-schema'
    ),
    path(
        'spectacular/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='spectacular-docs'
    ),
]
