class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False


class UserScope(Scope):
    allow_module = ['v1.token', 'v1.user', 'v1.mail']


class InactivateUserScope(Scope):
    allow_api = [
        'v1.token+get_token_api',  # 登录
        'v1.user+get_current_user_api',  # 获取当前登录用户
        'v1.mail+send_verification_mail_api'  # 发送验证邮件
    ]


class AdminScope(Scope):
    allow_module = ['v1.token', 'v1.user', 'v1.mail']
