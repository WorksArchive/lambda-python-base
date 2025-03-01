from access_control.access_control import AccessControlRole, AccessControlPermission
from typeguard import typechecked


@typechecked
class AccessControlAuditor:
    _instance = None
    _user = ''
    _role: list[AccessControlRole] = []

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AccessControlAuditor, cls).__new__(cls)
        return cls._instance

    @classmethod
    def setUser(cls, user: str):
        cls._user = user

    @classmethod
    def addRole(cls, role: AccessControlRole):
        cls._role.append(role)

    @classmethod
    def audit(cls, permission: AccessControlPermission):
        for role in cls._role:
            for perm in role.getPermissions():
                if perm == permission:
                    return True
        return False

    @classmethod
    def clear(cls):
        cls._role.clear()
