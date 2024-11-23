from aws_client.wnss_table import WNSs
from aws_lambda_powertools import Logger

logger = Logger(child=True)


def get_work(id: str) -> dict | None:
    work = WNSs.get_record_by_id(id, system_category="Works")
    return work
