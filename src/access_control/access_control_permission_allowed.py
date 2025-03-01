from access_control.access_control_auditor import AccessControlAuditor
from access_control.access_control import AccessControlPermissionFactory

from typeguard import typechecked


@typechecked
class AccessControlPermissionAllowed:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __call__(self, function):
        def _AccessControlPermissionAllowed_wrapper(*args, acpaVerify=False, **kwargs):
            ret = None
            if len(self._args) >= 2:
                ret = self._args[1]
            acpaVerify = acpaVerify or AccessControlAuditor.audit(
                AccessControlPermissionFactory.getPermission(self._args[0])
            )
            if function.__name__ == "_AccessControlPermissionAllowed_wrapper":
                ret = function(*args, acpaVerify=acpaVerify, **kwargs)
            elif acpaVerify:
                ret = function(*args, **kwargs)
            return ret
        return _AccessControlPermissionAllowed_wrapper
