from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import Group, Permission, ContentType

from .serializers import UserSerializer, PermSerializer, GroupSerializer
from utils.exceptions import InvalidPassword, PermissionDenied, ValidationError, WrongPassword


_exclude_content_model = ('logentry', 'contenttype', 'session', 'itemplans')
_exclude_contenttypes = [c.id for c in ContentType.objects.filter(
    model__in=_exclude_content_model
)]  # 排除掉Django内建应用和不需要的权限


class RoleViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(['GET'], detail=True, url_path='perms')
    def perms(self, request, pk):
        if request.user.has_perm('auth.view_permission'):
            obj = self.get_object()
            data = GroupSerializer(obj).data  # 当前角色和其权限ids
            # 系统内全部权限
            app_label_set = \
                list({i.get('app_label') for i in ContentType.objects.exclude(model__in=_exclude_content_model)
                     .values('app_label')})
            data['allPerms'] = []
            for app_label in app_label_set:
                tmp_data = {'id': app_label, 'name': app_label}
                query_set = PermViewSet.queryset.filter(
                    content_type__app_label=app_label).values('id', 'name', 'content_type__app_label')
                tmp_data['children'] = [{'id': i.get('id'), 'name': i.get('name')} for i in query_set]
                data['allPerms'].append(tmp_data)
            return Response(data)
        raise PermissionDenied

    def partial_update(self, request, *args, **kwargs):
        # 去掉父节点
        request.data['permissions'] = [i for i in request.data['permissions'] if isinstance(i, int)]
        return super().partial_update(request, *args, **kwargs)


class PermViewSet(ReadOnlyModelViewSet):
    queryset = Permission.objects.exclude(content_type__in=_exclude_contenttypes)\
        .exclude(codename__in=['add_permission', 'change_permission', 'delete_permission']).order_by('id')
    serializer_class = PermSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'codename']


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)  # 剔除不要更新的字段
        request.data.pop('id', None)
        request.data.pop('password', None)
        # 只有admin用户才能修改admin
        if request.data.get('is_superuser', None) and not request.user.is_superuser:
            raise PermissionDenied
        return super().partial_update(request, *args, **kwargs)

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                raise NotFound
        return super().get_object()

    @action(detail=True, methods=['GET'], url_path='roles')
    def roles(self, request, pk=None):  # /users/mgt/2/roles/ GET
        user = self.get_object()
        data = UserSerializer(user).data
        data['roles'] = [r.get('id') for r in user.groups.values('id')]
        data['allRoles'] = Group.objects.values('id', 'name')
        return Response(data)

    @roles.mapping.put  # /users/mgt/2/roles/ PUT
    def set_roles(self, request, pk=None):
        user = self.get_object()
        roles = request.data.get('roles', [])
        user.groups.set(roles)
        return Response(status=201)


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
    if request.user.has_perm('user.view_userprofile'):
        item = MenuItem(1, '用户管理')
        item.append(MenuItem(101, '用户列表', '/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))
        menulist.append(item)
    item = MenuItem(2, '项目组')
    item.append(MenuItem(201, '项目管理', '/items'))
    menulist.append(item)
    return Response(menulist)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):  # detail=False，uri不能带参数
    return Response({
        'user': {
            'id': request.user.id,
            'username': request.user.username
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    # detail=True uri能带参数 <pk>/chpwd/
    user = request.user
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
