from typing import Any, Generator
from aws_client.wnss_table import WNSs
from biz.works import Works
from moto import mock_aws
import pytest
import datetime
from access_control.access_control_auditor import AccessControlAuditor
from access_control.access_control import (
    AccessControlPermissionFactory,
    AccessControlRole,
)
from pytest_mock import MockFixture


@pytest.fixture(scope="session", autouse=True)
def test_works_mock_dynamodb():
    """DynamoDBをモック化する"""
    mock_aws().start()
    yield
    mock_aws().stop()


@pytest.fixture(scope="module", autouse=True)
def test_works_table():
    """テーブル作成"""
    response = WNSs.create_table()
    print(response)
    yield
    WNSs.delete_table()


@pytest.fixture(scope="function")
def test_works_a() -> Generator[WNSs, Any, None]:
    """id=aのレコード作成"""
    table: WNSs = WNSs(
        hash_key="hash_key A",
        range_key="range_key A",
        system_category="Works",
        cms_id="cms_id A",
        type="type A",
        registration_date=datetime.datetime(
            year=2024,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
        work_url="work_url",
        public=True,
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


def test_wnss_get1(test_works_a: WNSs, mocker: MockFixture):
    mock_instance = mocker.MagicMock()
    mocker.patch("biz.works.WnssEndpoint", return_value=mock_instance)
    mocker.patch(
        "biz.works.WnssEndpoint.get_contents",
        return_value={},
    )

    AccessControlAuditor.clear()
    role = AccessControlRole()
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_GENERAL"))
    AccessControlAuditor.addRole(role)

    actual = Works.get_work(test_works_a.id)

    exp = test_works_a.attribute_values
    exp.pop("work_url")
    exp.pop("public")
    assert exp == actual


def test_wnss_get2(test_works_a: WNSs, mocker: MockFixture):
    mock_instance = mocker.MagicMock()
    mocker.patch("biz.works.WnssEndpoint", return_value=mock_instance)
    mocker.patch(
        "biz.works.WnssEndpoint.get_contents",
        return_value={},
    )

    AccessControlAuditor.clear()
    role = AccessControlRole()
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_GENERAL"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_LOGIN"))
    AccessControlAuditor.addRole(role)

    actual = Works.get_work(test_works_a.id)

    exp = test_works_a.attribute_values
    exp.pop("work_url")
    exp.pop("public")
    assert exp == actual


def test_wnss_get3(test_works_a: WNSs, mocker: MockFixture):
    mock_instance = mocker.MagicMock()
    mocker.patch("biz.works.WnssEndpoint", return_value=mock_instance)
    mocker.patch(
        "biz.works.WnssEndpoint.get_contents",
        return_value={},
    )

    AccessControlAuditor.clear()
    role = AccessControlRole()
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_GENERAL"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_LOGIN"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_BUY"))
    AccessControlAuditor.addRole(role)

    actual = Works.get_work(test_works_a.id)

    exp = test_works_a.attribute_values
    exp.pop("public")
    assert exp == actual


def test_wnss_get4(test_works_a: WNSs, mocker: MockFixture):
    mock_instance = mocker.MagicMock()
    mocker.patch("biz.works.WnssEndpoint", return_value=mock_instance)
    mocker.patch(
        "biz.works.WnssEndpoint.get_contents",
        return_value={},
    )

    AccessControlAuditor.clear()
    role = AccessControlRole()
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_GENERAL"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_LOGIN"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_BUY"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_OWNER"))
    AccessControlAuditor.addRole(role)

    actual = Works.get_work(test_works_a.id)

    exp = test_works_a.attribute_values
    assert exp == actual


def test_wnss_get5(test_works_a: WNSs, mocker: MockFixture):
    mock_instance = mocker.MagicMock()
    mocker.patch("biz.works.WnssEndpoint", return_value=mock_instance)
    mocker.patch(
        "biz.works.WnssEndpoint.get_contents",
        return_value={},
    )

    AccessControlAuditor.clear()
    role = AccessControlRole()
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_GENERAL"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_LOGIN"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_BUY"))
    role.addPermission(AccessControlPermissionFactory.getPermission("READ_OWNER"))
    AccessControlAuditor.addRole(role)

    actual = Works.get_work("dummy")

    exp = None
    assert exp == actual
