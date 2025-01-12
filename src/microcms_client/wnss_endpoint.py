from typeguard import typechecked

from microcms_client.microcms import MicroCMS
from aws_client.parameter_store import get_parameter


@typechecked
class WnssEndpoint(MicroCMS):
    def __init__(cls):
        super().__init__(get_parameter("MICRO_CMS_ENDPOINT_WNSS"))
