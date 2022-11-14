import re
from rest_framework import serializers
from django.contrib.auth.models import make_password, Group, Permission, ContentType

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    checkPass = serializers.CharField(required=True, max_length=16, min_length=6, write_only=True, )

    class Meta:
        model = UserProfile
        fields = (
            'id', "password", "is_superuser", "username",
            "email", "is_active", "phone", "checkPass"
            # 'groups', 'user_permissions'
        )

        extra_kwargs = {
            'username': {'max_length': 16, "min_length": 3},  # 重新限定用户名长度
            'password': {"write_only": True},
            'is_superuser': {'default': False},
            'is_active': {'default': False}
        }

    def validate_password(self, value):
        # 验证密码
        if 6 <= len(value) <= 16:
            if self.initial_data['checkPass'] == value:
                return make_password(value)
            raise serializers.ValidationError("The passwords do not match")
        raise serializers.ValidationError("The length of password must be between 6 and 16")

    def validate_username(self, value):
        # 验证用户名
        if UserProfile.objects.filter(username=value).count():
            raise serializers.ValidationError("user already exists")
        return value

    def validate_phone(self, value):
        if value:
            phone = "^[9][0-9]{9}$"
            if not re.match(phone, value):
                raise serializers.ValidationError("what is this phone?")
        return value

    def validate(self, attrs):
        # 表里没有checkPass字段，只是验证用的，所以验证完成后删掉，不需要提交到库
        try:
            del attrs['checkPass']
        finally:
            return attrs


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    django 内置关联表, 能看到prem表和其他表的关联信息
    """
    class Meta:
        model = ContentType
        fields = '__all__'


class PermSerializer(serializers.ModelSerializer):
    """
    权限
    {
        "id": 21,
        "content_type": {
            "id": 6,
            "app_label": "user",
            "model": "userprofile"
        },
        "name": "Can add 用户详细信息",
        "codename": "add_userprofile"
    },
    """
    class Meta:
        model = Permission
        fields = '__all__'

    content_type = ContentTypeSerializer(read_only=True)  # 嵌套序列化器


class GroupSerializer(serializers.ModelSerializer):
    """
    permissions = [1, 2, ..., permissions表ManyToMany id]
    角色
    """

    class Meta:
        model = Group
        fields = '__all__'
