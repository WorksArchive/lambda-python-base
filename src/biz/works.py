from aws_client.wnss_table import WNSs
from aws_lambda_powertools import Logger
from access_control.access_control_permission_allowed import (
    AccessControlPermissionAllowed,
)
from microcms_client.wnss_endpoint import WnssEndpoint
from enum import IntEnum
from typing import Any

logger = Logger(child=True)


class Works:
    class ACCESS_TYPE(IntEnum):
        GENERAL = 0
        LOGIN = 1
        BUY = 2
        OWNER = 3

    # fmt: off
    READ_ACCESS: dict[str, list[bool]] = {
        # GENERAL, LOGIN, BUY, OWNER
        # AWS
        "user_id": [True, True, True, True, ],
        "id": [True, True, True, True, ],
        "system_category": [True, True, True, True, ],
        "cms_id": [True, True, True, True, ],
        "numbering_id": [True, True, True, True, ],
        "series_id": [True, True, True, True, ],
        "type": [True, True, True, True, ],
        "subtype": [True, True, True, True, ],
        "price": [True, True, True, True, ],
        "pages": [True, True, True, True, ],
        "original_id": [True, True, True, True, ],
        "registration_date": [True, True, True, True, ],
        "version": [True, True, True, True, ],
        "printing_office": [True, True, True, True, ],
        "sales_locations_url": [True, True, True, True, ],
        "format": [True, True, True, True, ],
        "r18": [True, True, True, True, ],
        "r18g": [True, True, True, True, ],
        "isbn": [True, True, True, True, ],
        "language": [True, True, True, True, ],
        "work_url": [False, False, True, True, ],
        "selling_price": [True, True, True, True, ],
        "extension": [True, True, True, True, ],
        "public": [False, False, False, True, ],
        "progress": [True, True, True, True, ],
        "subscription": [True, True, True, True, ],
        "page_view": [True, True, True, True, ],
        "favorites": [True, True, True, True, ],
        "update_information": [True, True, True, True, ],
        "numbering_order": [True, True, True, True, ],
        "thumbnail": [True, True, True, True, ],
        # MicroCMS
        "title": [True, True, True, True, ],
        "description": [True, True, True, True, ],
        "summary": [True, True, True, True, ],
        "owner": [True, True, True, True, ],
        "authors": [True, True, True, True, ],
        "circle": [True, True, True, True, ],
        "piblisher": [True, True, True, True, ],
        "characters": [True, True, True, True, ],
        "original": [True, True, True, True, ],
        "genre": [True, True, True, True, ],
        "issue_date": [True, True, True, True, ],
        "update_date": [True, True, True, True, ],
        "first_event": [True, True, True, True, ],
        "medias": [True, True, True, True, ],
        "sales_locations": [True, True, True, True, ],
        "series": [True, True, True, True, ],
        "numbering": [True, True, True, True, ],
        "tags": [True, True, True, True, ],
        "works": [True, True, True, True, ],
    }
    # fmt: on

    @staticmethod
    def get_work(id: str) -> dict | None:
        ret: dict[str, Any] = {}
        work = WNSs.get_record_by_id(id, system_category="Works")
        if work is not None:
            cms_endpoint = WnssEndpoint()
            work |= cms_endpoint.get_contents(work["cms_id"])
            ret |= Works.get_work_read_general(work)
            ret |= Works.get_work_read_login(work)
            ret |= Works.get_work_read_buy(work)
            ret |= Works.get_work_read_owner(work)
        if len(ret) == 0:
            return None
        return ret

    @staticmethod
    @AccessControlPermissionAllowed("READ_GENERAL", {})
    def get_work_read_general(work) -> dict:
        ret = {}
        for key in Works.READ_ACCESS.keys():
            if Works.READ_ACCESS[key][Works.ACCESS_TYPE.GENERAL]:
                if key in work:
                    ret[key] = work[key]
        return ret

    @staticmethod
    @AccessControlPermissionAllowed("READ_LOGIN", {})
    def get_work_read_login(work) -> dict:
        ret = {}
        for key in Works.READ_ACCESS.keys():
            if Works.READ_ACCESS[key][Works.ACCESS_TYPE.LOGIN]:
                if key in work:
                    ret[key] = work[key]
        return ret

    @staticmethod
    @AccessControlPermissionAllowed("READ_BUY", {})
    def get_work_read_buy(work) -> dict:
        ret = {}
        for key in Works.READ_ACCESS.keys():
            if Works.READ_ACCESS[key][Works.ACCESS_TYPE.BUY]:
                if key in work:
                    ret[key] = work[key]
        return ret

    @staticmethod
    @AccessControlPermissionAllowed("READ_OWNER", {})
    def get_work_read_owner(work) -> dict:
        ret = {}
        for key in Works.READ_ACCESS.keys():
            if Works.READ_ACCESS[key][Works.ACCESS_TYPE.OWNER]:
                if key in work:
                    ret[key] = work[key]
        return ret
