from typing import Any, Generator
from aws_client.wnss_table import WNSs
from moto import mock_aws
import pytest
import datetime


@pytest.fixture(scope="session", autouse=True)
def test_wnss_mock_dynamodb():
    """DynamoDBをモック化する"""
    mock_aws().start()
    yield
    mock_aws().stop()


@pytest.fixture(scope="module", autouse=True)
def test_wnss_table():
    """テーブル作成"""
    response = WNSs.create_table()
    print(response)
    yield
    WNSs.delete_table()


@pytest.fixture(scope="function")
def test_wnss_a() -> Generator[WNSs, Any, None]:
    """id=aのレコード作成"""
    table: WNSs = WNSs(
        hash_key="hash_key A",
        range_key="range_key A",
        system_category="system_category A",
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
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


@pytest.fixture(scope="function")
def test_wnss_b() -> Generator[WNSs, Any, None]:
    """id=bのレコード作成"""
    table: WNSs = WNSs(
        hash_key="hash_key B",
        range_key="range_key B",
        system_category="system_category B",
        cms_id="cms_id B",
        type="type B",
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
def test_wnss_c() -> Generator[WNSs, Any, None]:
    """id=cのレコード作成"""
    table: WNSs = WNSs(
        hash_key="hash_key C",
        range_key="range_key C",
        system_category="system_category C",
        cms_id="cms_id C",
        type="type C",
        registration_date=datetime.datetime(
            year=2024,
            month=3,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc,
        ),
        numbering_id="numbering_id C",
        series_id="series_id C",
    )
    save_result: dict[str, Any] = table.save()
    print(save_result)
    yield table
    table.delete()


def test_wnss_get(test_wnss_a: WNSs):
    actual = WNSs.get(hash_key=test_wnss_a.user_id, range_key=test_wnss_a.id)
    assert hash(test_wnss_a) != hash(actual)
    assert test_wnss_a.attribute_values == actual.attribute_values


def test_wnss_get_record1(test_wnss_a: WNSs):
    record = WNSs.get_record(test_wnss_a.user_id, test_wnss_a.id)
    assert test_wnss_a.attribute_values == record


def test_wnss_get_record2(test_wnss_b: WNSs):
    record = WNSs.get_record(test_wnss_b.user_id)
    assert test_wnss_b.attribute_values == record


def test_wnss_get_record3(test_wnss_c: WNSs):
    record = WNSs.get_record("hash_key D")
    assert record is None


def test_wnss_get_record_by_cms_id1(test_wnss_a: WNSs):
    record = WNSs.get_record_by_cms_id(test_wnss_a.cms_id, test_wnss_a.system_category)
    assert test_wnss_a.attribute_values == record


def test_wnss_get_record_by_cms_id2(test_wnss_b: WNSs):
    record = WNSs.get_record_by_cms_id(test_wnss_b.cms_id)
    assert test_wnss_b.attribute_values == record


def test_wnss_get_record_by_cms_id3(test_wnss_c: WNSs):
    record = WNSs.get_record_by_cms_id("hash_key D")
    assert record is None


def test_wnss_get_record_by_id1(test_wnss_a: WNSs):
    record = WNSs.get_record_by_id(test_wnss_a.id, test_wnss_a.system_category)
    assert test_wnss_a.attribute_values == record


def test_wnss_get_record_by_id2(test_wnss_b: WNSs):
    record = WNSs.get_record_by_id(test_wnss_b.id)
    assert test_wnss_b.attribute_values == record


def test_wnss_get_record_by_id3(test_wnss_c: WNSs):
    record = WNSs.get_record_by_id("hash_key D")
    assert record is None


def test_wnss_get_record_by_numbering_id1(test_wnss_c: WNSs):
    record = WNSs.get_record_by_numbering_id(test_wnss_c.numbering_id)
    assert test_wnss_c.attribute_values == record


def test_wnss_get_record_by_numbering_id2(test_wnss_a: WNSs):
    record = WNSs.get_record_by_numbering_id("hash_key D")
    assert record is None


def test_wnss_get_record_by_series_id1(test_wnss_c: WNSs):
    record = WNSs.get_record_by_series_id(
        test_wnss_c.series_id, test_wnss_c.system_category
    )
    assert test_wnss_c.attribute_values == record


def test_wnss_get_record_by_series_id2(test_wnss_c: WNSs):
    record = WNSs.get_record_by_series_id(test_wnss_c.series_id)
    assert test_wnss_c.attribute_values == record


def test_wnss_get_record_by_series_id3(test_wnss_a: WNSs):
    record = WNSs.get_record_by_series_id("hash_key D")
    assert record is None
