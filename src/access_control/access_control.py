from typeguard import typechecked


@typechecked
class AccessControlPermission:
    def __init__(self, id: str):
        self._id = id

    def __eq__(self, other):
        return self._id == other._id


@typechecked
class AccessControlPermissionFactory:
    _instance = None
    _pool: dict[str, AccessControlPermission] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AccessControlPermissionFactory, cls).__new__(cls)
        return cls._instance

    @classmethod
    def getPermission(cls, id: str):
        if id in cls._pool:
            return cls._pool[id]
        cls._pool[id] = AccessControlPermission(id)
        return cls._pool[id]


@typechecked
class AccessControlRole:
    def __init__(self):
        self._permission = []

    def addPermission(self, permission: AccessControlPermission):
        self._permission.append(permission)

    def getPermissions(self):
        return self._permission
