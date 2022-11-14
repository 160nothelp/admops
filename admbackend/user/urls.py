from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import menulist_view, UserViewSet, PermViewSet, RoleViewSet


router = SimpleRouter()
router.register('mgt', UserViewSet)
router.register('perms', PermViewSet)
router.register('roles', RoleViewSet)


urlpatterns = [
    path('menulist/', menulist_view),
] + router.urls
