from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ItemsViewSet, ItemPlansViewSet


router = SimpleRouter()
router.register('item_mgt', ItemsViewSet)
router.register('item_plan', ItemPlansViewSet)


urlpatterns = router.urls
