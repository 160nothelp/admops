from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import Group, Permission, ContentType

from .serializers import UserSerializer, PermSerializer, GroupSerializer
from utils.exceptions import InvalidPassword
from utils.exceptions import ValidationError
from utils.exceptions import WrongPassword

_exclude_contenttypes = [c.id for c in ContentType.objects.filter(
    model__in=['logentry', 'group', 'permission', 'contenttype', 'session']
)]  # 排除掉Django内建应用的权限


class RoleViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(['GET'], detail=True, url_path='perms')
    def perms(self, request, pk):
        obj = self.get_object()
        data = GroupSerializer(obj).data  # 当前角色和其权限ids
        # 系统内全部权限
        app_label_set = \
            list({i.get('content_type__app_label') for i in PermViewSet.queryset.values('content_type__app_label')})
        data['allPerms'] = \
            [{'id': app_label, 'name': app_label, 'children':
                [{'id': i.get('id'), 'name': i.get('name')}
                 for i in PermViewSet.queryset.values('id', 'name', 'content_type__app_label')
                 if i.get('content_type__app_label') == app_label]} for app_label in app_label_set]
        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        request.data['permissions'] = [i for i in request.data['permissions'] if isinstance(i, int)]
        return super().partial_update(request, *args, **kwargs)


class PermViewSet(ReadOnlyModelViewSet):
    queryset = Permission.objects.exclude(content_type__in=_exclude_contenttypes)
    serializer_class = PermSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'codename']


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser] # 必须是管理员才能管理用户
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)  # 剔除不要更新的字段
        request.data.pop('id', None)
        request.data.pop('password', None)
        return super().partial_update(request, *args, **kwargs)

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                raise NotFound
        return super().get_object()

    @action(['GET'], detail=False, url_path='whoami')
    def whoami(self, request):  # detail=False，uri不能带参数
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username
            }
        })

    @action(detail=True, methods=['post'], url_path='chpwd')
    def change_password(self, request, pk=None):
        # detail=True uri能带参数 <pk>/chpwd/
        user = self.get_object()  # 能不能使用request.user
        if user.check_password(request.data['oldPassword']):
            if request.data['password'] == request.data['checkPass']:
                if user.check_password(request.data['password']):
                    # 说明新密码和旧密码相同
                    raise WrongPassword
                user.set_password(request.data['password'])
                user.save()
                return Response()
            else:
                raise ValidationError
        else:
            raise InvalidPassword


class MenuItem(dict):
    def __init__(self, id, name, path=None):
        super().__init__()
        self['id'] = id
        self['name'] = name
        self['path'] = path
        self['children'] = []

    def append(self, item):
        self['children'].append(item)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 覆盖全局配置
def menulist_view(request):
    menulist = []
    if request.user.is_superuser:  # 用户管理必须管理员
        item = MenuItem(1, '用户管理')
        item.append(MenuItem(101, '用户列表', '/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))
        menulist.append(item)
    return Response(menulist)
