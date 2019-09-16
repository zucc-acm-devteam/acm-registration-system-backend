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
    allow_module = ['v1.token', 'v1.user', 'v1.captcha', 'v1.team', 'v1.team_relationship']
    allow_api = [
        'v1.contest+get_contest_api',
        'v1.contest+search_contest_api',
        'v1.announcement+get_announcement_api',
        'v1.announcement+search_announcement_api',
    ]


class IncompleteUserScope(Scope):  # 未注册完成用户
    allow_module = ['v1.token', 'v1.captcha']
    allow_api = [
        'v1.user+activate_user_api',
        'v1.user+modify_user_api',
        'v1.user+get_user_api'
    ]


class AdminScope(Scope):
    allow_module = ['v1.token', 'v1.user', 'v1.captcha', 'v1.contest', 'v1.team', 'v1.announcement',
                    'v1.team_relationship']
