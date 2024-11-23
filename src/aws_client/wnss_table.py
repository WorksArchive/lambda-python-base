from __future__ import annotations
from typing import Optional
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UTCDateTimeAttribute,
    UnicodeSetAttribute,
    BooleanAttribute,
)

from typeguard import typechecked


@typechecked
class ByCmsId(GlobalSecondaryIndex):
    class Meta:
        index_name = "ByCmsId"
        write_capacity_units = 10
        read_capacity_units = 10
        projection = AllProjection()

    cms_id = UnicodeAttribute(hash_key=True)
    system_category = UnicodeAttribute(range_key=True)


@typechecked
class ById(GlobalSecondaryIndex):
    class Meta:
        index_name = "ById"
        write_capacity_units = 10
        read_capacity_units = 10
        projection = AllProjection()

    id = UnicodeAttribute(hash_key=True)
    system_category = UnicodeAttribute(range_key=True)


@typechecked
class ByNumberingId(GlobalSecondaryIndex):
    class Meta:
        index_name = "ByNumberingId"
        write_capacity_units = 10
        read_capacity_units = 10
        projection = AllProjection()

    numbering_id = UnicodeAttribute(hash_key=True)


@typechecked
class BySeriesId(GlobalSecondaryIndex):
    class Meta:
        index_name = "BySeriesId"
        write_capacity_units = 10
        read_capacity_units = 10
        projection = AllProjection()

    series_id = UnicodeAttribute(hash_key=True)
    system_category = UnicodeAttribute(range_key=True)


@typechecked
class WNSs(Model):
    class Meta:
        table_name = "WNSs"
        region = "ap-northeast-1"
        write_capacity_units = 10
        read_capacity_units = 10

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)

    system_category = UnicodeAttribute(null=False)
    cms_id = UnicodeAttribute(null=False)
    numbering_id = UnicodeAttribute(null=True)
    series_id = UnicodeAttribute(null=True)
    type = UnicodeAttribute(null=False)
    subtype = UnicodeAttribute(null=True)
    price = NumberAttribute(null=True)
    pages = NumberAttribute(null=True)
    original_id = UnicodeAttribute(null=True)
    registration_date = UTCDateTimeAttribute(null=False)
    version = UnicodeAttribute(null=True)
    printing_office = UnicodeAttribute(null=True)
    sales_locations_url = UnicodeSetAttribute(null=True)
    format = UnicodeAttribute(null=True)
    r18 = BooleanAttribute(null=True)
    r18g = BooleanAttribute(null=True)
    isbn = UnicodeAttribute(null=True)
    language = UnicodeAttribute(null=True)
    work_url = UnicodeAttribute(null=True)
    selling_price = NumberAttribute(null=True)
    extension = UnicodeAttribute(null=True)
    public = BooleanAttribute(null=True)
    progress = UnicodeAttribute(null=True)
    subscription = BooleanAttribute(null=True)
    page_view = NumberAttribute(null=True)
    favorites = NumberAttribute(null=True)
    update_information = UnicodeAttribute(null=True)
    numbering_order = UnicodeSetAttribute(null=True)
    thumbnail = UnicodeAttribute(null=True)

    by_cms_id = ByCmsId()
    by_id = ById()
    by_numbering_id = ByNumberingId()
    by_series_id = BySeriesId()

    @classmethod
    def get_record(cls, user_id: str, id: Optional[str] = None) -> dict | None:
        retval = None
        condition = None if id is None else WNSs.id == id
        for item in WNSs.query(user_id, condition):
            retval = item.attribute_values
            break
        return retval

    @classmethod
    def get_record_by_cms_id(
        cls, cms_id: str, system_category: Optional[str] = None
    ) -> dict | None:
        retval = None
        condition = (
            None if system_category is None else WNSs.system_category == system_category
        )
        for item in WNSs.by_cms_id.query(cms_id, condition):
            retval = item.attribute_values
        return retval

    @classmethod
    def get_record_by_id(
        cls, id: str, system_category: Optional[str] = None
    ) -> dict | None:
        retval = None
        condition = (
            None if system_category is None else WNSs.system_category == system_category
        )
        for item in WNSs.by_id.query(id, condition):
            retval = item.attribute_values
        return retval

    @classmethod
    def get_record_by_numbering_id(cls, numbering_id: str) -> dict | None:
        retval = None
        for item in WNSs.by_numbering_id.query(numbering_id):
            retval = item.attribute_values
        return retval

    @classmethod
    def get_record_by_series_id(
        cls, series_id: str, system_category: Optional[str] = None
    ) -> dict | None:
        retval = None
        condition = (
            None if system_category is None else WNSs.system_category == system_category
        )
        for item in WNSs.by_series_id.query(series_id, condition):
            retval = item.attribute_values
        return retval
