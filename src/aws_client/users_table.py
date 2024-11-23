from __future__ import annotations
from typing import Optional
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    BooleanAttribute,
    UTCDateTimeAttribute,
    UnicodeSetAttribute,
)

from typeguard import typechecked


@typechecked
class Users(Model):
    class Meta:
        table_name = "Users"
        region = "ap-northeast-1"
        write_capacity_units = 10
        read_capacity_units = 10

    user_id = UnicodeAttribute(hash_key=True)
    cms_id = UnicodeAttribute(range_key=True)

    icon = UnicodeAttribute(null=True)
    header_image = UnicodeAttribute(null=True)
    sns_account = UnicodeAttribute(null=True)
    sns_account_url = UnicodeAttribute(null=True)
    age = NumberAttribute(null=True)
    age_public = BooleanAttribute(null=True)
    gender = UnicodeAttribute(null=True)
    gender_public = BooleanAttribute(null=True)
    birthday = UTCDateTimeAttribute(null=True)
    birthday_public = BooleanAttribute(null=True)
    business_public = BooleanAttribute(null=True)
    area_public = BooleanAttribute(null=True)
    email = UnicodeAttribute(null=True)
    registration_date = UTCDateTimeAttribute(null=False)
    website = UnicodeAttribute(null=True)
    masterpiece_id = UnicodeSetAttribute(null=True)
    weak_genre = UnicodeAttribute(null=True)
    language = UnicodeAttribute(null=True)
    selling_url = UnicodeAttribute(null=True)
    follower_ids = UnicodeSetAttribute(null=True)
    pickup_ids = UnicodeSetAttribute(null=True)
    works_bought_ids = UnicodeSetAttribute(null=True)
    favorite_ids = UnicodeSetAttribute(null=True)

    @classmethod
    def get_record(cls, user_id: str, cms_id: Optional[str] = None) -> dict | None:
        retval = None
        condition = None if cms_id is None else Users.cms_id == cms_id
        for item in Users.query(user_id, condition):
            retval = item.attribute_values
            break
        return retval
