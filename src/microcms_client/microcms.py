import requests
import json
from typeguard import typechecked

from aws_client.parameter_store import get_parameter


@typechecked
class MicroCMS:
    url = get_parameter("MICRO_CMS_URL")
    endpoint = ""
    api_key = get_parameter("MICRO_CMS_API_KEY")

    def __init__(cls, endpoint):
        cls.endpoint = endpoint

    @classmethod
    def get_contents(cls, contents_id: str) -> dict:
        retval = {}
        url = cls.url + cls.endpoint + '/' + contents_id
        headers = {'X-MICROCMS-API-KEY': cls.api_key}

        res = requests.get(url, headers=headers)
        if res.status_code == requests.codes.ok:
            retval = json.loads(res.text)

        return retval
