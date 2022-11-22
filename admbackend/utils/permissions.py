from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoModelPermissions


class RealIsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CustomModelPermission(DjangoModelPermissions):
    # 和应用的Model类的增删改查对应
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  # 增加view查看权限GET
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
