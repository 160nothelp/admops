from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status


# 只要有错误码小于100都和登录有关
class CustomBaseException(exceptions.APIException):
    code = 10000  # code为0表示正常，非0都是异常
    message = "未知错误，请联系管理员"

    @classmethod
    def get_message(cls):
        return {'code': cls.code, 'message': cls.message}


class InvalidUsernameOrPassword(CustomBaseException):
    code = 1
    message = '用户名或密码错误，请重新登录'


class NotAuthenticated(CustomBaseException):
    code = 2
    message = '认证失败，请重新登录'


class InvalidToken(CustomBaseException):
    code = 3
    message = '认证过期，请重新登录'


class InvalidPassword(CustomBaseException):
    code = 101
    message = '密码验证错误'


class WrongPassword(CustomBaseException):
    code = 102
    message = '新密码不能和旧密码相同'


class ValidationError(CustomBaseException):
    code = 10001
    message = '数据验证失败'


class NotFound(CustomBaseException):
    code = 10002
    message = 'Not Found Something'


# Django Drf异常类 我要做映射和替换
exc_map = {
    'AuthenticationFailed': InvalidUsernameOrPassword,
    'NotAuthenticated': NotAuthenticated,
    'InvalidToken': InvalidToken,
    'ValidationError': ValidationError,
    'NotFound': NotFound,
}


def custom_exception_handler(exc, context):
    print(exc, type(exc), '!!!!!!!!!!!!!!!!!!!!!!!!!!')
    response = exception_handler(exc, context)
    print('~' * 30)
    print(type(exc), exc.__dict__)
    print('~' * 30)

    if response is not None:
        # 提供最终用户更加友好的提示、阻止某些技术导致的异常信息返回
        # 从一种异常类型 映射 到另一种异常
        if isinstance(exc, CustomBaseException):
            errmsg = exc.get_message()
        else:
            errmsg = exc_map.get(exc.__class__.__name__, CustomBaseException).get_message()
            print(errmsg)
        return Response(errmsg, status=status.HTTP_200_OK)  # 恒为200
    return response
