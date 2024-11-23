from typing import Any, Generator
from aws_client.users_table import Users
from moto import mock_aws
import pytest
import datetime


@pytest.fixture(scope="session", autouse=True)
def test_users_mock_dynamodb():
    """DynamoDBをモック化する"""
    mock_aws().start()
    yield
    mock_aws().stop()


@pytest.fixture(scope="module", autouse=True)
def test_users_table():
    """テーブル作成"""
    response = Users.create_table()
    print(response)
    yield
    Users.delete_table()


@pytest.fixture(scope="function")
def test_users_a() -> Generator[Users, Any, None]:
    """id=aのレコード作成"""
    table: Users = Users(
        hash_key="hash_key A",
        range_key="range_key A",
        registration_date=datetime.datetime(
            year=2024,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


@pytest.fixture(scope="function")
def test_users_b() -> Generator[Users, Any, None]:
    """id=bのレコード作成"""
    table: Users = Users(
        hash_key="hash_key B",
        range_key="range_key B",
        registration_date=datetime.datetime(
            year=2024,
            month=2,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


@pytest.fixture(scope="function")
def test_users_c() -> Generator[Users, Any, None]:
    """id=cのレコード作成"""
    table: Users = Users(
        hash_key="hash_key C",
        range_key="range_key C",
        registration_date=datetime.datetime(
            year=2024,
            month=3,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


def test_users_get(test_users_a: Users):
    actual = Users.get(hash_key=test_users_a.user_id, range_key=test_users_a.cms_id)
    assert hash(test_users_a) != hash(actual)
    assert test_users_a.attribute_values == actual.attribute_values


def test_users_get_record1(test_users_a: Users):
    record = Users.get_record(test_users_a.user_id, test_users_a.cms_id)
    assert test_users_a.attribute_values == record


def test_users_get_record2(test_users_b: Users):
    record = Users.get_record(test_users_b.user_id)
    assert test_users_b.attribute_values == record


def test_users_get_record3(test_users_c: Users):
    record = Users.get_record("hash_key D")
    assert record is None
