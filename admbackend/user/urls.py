from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, PermViewSet, RoleViewSet, menulist_view, whoami, change_password


router = SimpleRouter()
router.register('mgt', UserViewSet)
router.register('perms', PermViewSet)
router.register('roles', RoleViewSet)


urlpatterns = [
    path('meta/menulist/', menulist_view),
    path('meta/whoami/', whoami),
    path('meta/chpwd/', change_password),
] + router.urls
