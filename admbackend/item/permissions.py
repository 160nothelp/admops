from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .apps import ItemConfig
from .models import Items
from utils.exceptions import NotFound, ValidationError


class ItemsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' and request.path == '/items/item_plan/':
            try:
                item_name = request.query_params.get('item_name').split(',')
            except Exception:
                raise ValidationError
            if item_name is None:
                raise NotFound
            flag = True
            for id in item_name:
                codename = f'view_{Items.__name__}_{id}'
                flag = flag and request.user.has_perm(f'{ItemConfig.name}.{codename}')
            return flag
        return True
