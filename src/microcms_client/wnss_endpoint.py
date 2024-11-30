from typeguard import typechecked

from microcms_client.microcms import MicroCMS
from aws_client.parameter_store import get_parameter


@typechecked
class WnssEndpoint(MicroCMS):
    endpoint = get_parameter("MICRO_CMS_ENDPOINT_WNSS")

    def __init__(cls):
        super(cls.endpoint)
