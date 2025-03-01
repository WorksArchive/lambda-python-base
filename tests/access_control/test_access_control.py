from access_control.access_control_auditor import AccessControlAuditor
from access_control.access_control import (
    AccessControlPermissionFactory,
    AccessControlRole,
)
from access_control.access_control_permission_allowed import (
    AccessControlPermissionAllowed,
)
import pytest


@AccessControlPermissionAllowed("permissionA")
@AccessControlPermissionAllowed("permissionB")
def test_access_control_function1():
    return 1


@AccessControlPermissionAllowed("permissionA")
def test_access_control_function2():
    return 2


@AccessControlPermissionAllowed("permissionB")
def test_access_control_function3():
    return 3


@AccessControlPermissionAllowed("permissionC")
def test_access_control_function4():
    return 4


@AccessControlPermissionAllowed("permissionA", "A")
@AccessControlPermissionAllowed("permissionB", "B")
def test_access_control_function11():
    return 1


@AccessControlPermissionAllowed("permissionA", "C")
def test_access_control_function12():
    return 2


@AccessControlPermissionAllowed("permissionB", "D")
def test_access_control_function13():
    return 3


@AccessControlPermissionAllowed("permissionC", "E")
def test_access_control_function14():
    return 4


@AccessControlPermissionAllowed("permissionA", "A")
@AccessControlPermissionAllowed("permissionB", "B")
def test_access_control_function21(num: int):
    return num


@AccessControlPermissionAllowed("permissionA", "C")
def test_access_control_function22(num: int):
    return num


@AccessControlPermissionAllowed("permissionB", "D")
def test_access_control_function23(num: int):
    return num


@AccessControlPermissionAllowed("permissionC", "E")
def test_access_control_function24(num: int):
    return num


@pytest.mark.parametrize(
    ["perm1", "perm2", "perm3", "func1", "func2", "func3", "func4"],
    [
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            1,
            2,
            3,
            None,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            None,
            None,
            1,
            2,
            None,
            None,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            None,
            1,
            None,
            3,
            None,
        ),
        pytest.param(
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            None,
            None,
            None,
            None,
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            1,
            2,
            None,
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            1,
            2,
            3,
            4,
        ),
    ],
)
def test_access_control(perm1, perm2, perm3, func1, func2, func3, func4):
    AccessControlAuditor.clear()
    role = AccessControlRole()
    if perm1 is not None:
        role.addPermission(perm1)
    if perm2 is not None:
        role.addPermission(perm2)
    if perm3 is not None:
        role.addPermission(perm3)
    AccessControlAuditor.addRole(role)
    ret1 = test_access_control_function1()
    ret2 = test_access_control_function2()
    ret3 = test_access_control_function3()
    ret4 = test_access_control_function4()
    assert ret1 == func1
    assert ret2 == func2
    assert ret3 == func3
    assert ret4 == func4


@pytest.mark.parametrize(
    ["perm1", "perm2", "perm3", "func1", "func2", "func3", "func4"],
    [
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            1,
            2,
            3,
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            None,
            None,
            1,
            2,
            "D",
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            None,
            1,
            "C",
            3,
            "E",
        ),
        pytest.param(
            None,
            None,
            None,
            "B",
            "C",
            "D",
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            None,
            "B",
            "C",
            "D",
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            1,
            2,
            "D",
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            1,
            2,
            3,
            4,
        ),
    ],
)
def test_access_control2(perm1, perm2, perm3, func1, func2, func3, func4):
    AccessControlAuditor.clear()
    role = AccessControlRole()
    if perm1 is not None:
        role.addPermission(perm1)
    if perm2 is not None:
        role.addPermission(perm2)
    if perm3 is not None:
        role.addPermission(perm3)
    AccessControlAuditor.addRole(role)
    ret1 = test_access_control_function11()
    ret2 = test_access_control_function12()
    ret3 = test_access_control_function13()
    ret4 = test_access_control_function14()
    assert ret1 == func1
    assert ret2 == func2
    assert ret3 == func3
    assert ret4 == func4


@pytest.mark.parametrize(
    ["perm1", "perm2", "perm3", "func1", "func2", "func3", "func4"],
    [
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            1,
            2,
            3,
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            None,
            None,
            1,
            2,
            "D",
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionB"),
            None,
            None,
            1,
            "C",
            3,
            "E",
        ),
        pytest.param(
            None,
            None,
            None,
            "B",
            "C",
            "D",
            "E",
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            None,
            "B",
            "C",
            "D",
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            None,
            1,
            2,
            "D",
            4,
        ),
        pytest.param(
            AccessControlPermissionFactory.getPermission("permissionA"),
            AccessControlPermissionFactory.getPermission("permissionC"),
            AccessControlPermissionFactory.getPermission("permissionB"),
            1,
            2,
            3,
            4,
        ),
    ],
)
def test_access_control3(perm1, perm2, perm3, func1, func2, func3, func4):
    AccessControlAuditor.clear()
    role = AccessControlRole()
    if perm1 is not None:
        role.addPermission(perm1)
    if perm2 is not None:
        role.addPermission(perm2)
    if perm3 is not None:
        role.addPermission(perm3)
    AccessControlAuditor.addRole(role)
    ret1 = test_access_control_function21(1)
    ret2 = test_access_control_function22(2)
    ret3 = test_access_control_function23(3)
    ret4 = test_access_control_function24(4)
    assert ret1 == func1
    assert ret2 == func2
    assert ret3 == func3
    assert ret4 == func4
