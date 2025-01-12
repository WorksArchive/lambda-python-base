import json

from typing import Any
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from biz import artwork, wnss
from microcms_client.wnss_endpoint import WnssEndpoint
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from datetime import date, datetime

app = APIGatewayRestResolver()
logger = Logger(child=True)


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {obj} not serializable")


@app.get("/artworks")
def get_artworks() -> dict[str, Any]:
    # TODO: pydanticなどでレスポンスモデル作成
    return {"artworks": artwork.get_artworks()}


@app.get("/info")
def get_info() -> dict[str, Any]:
    return {"message": "KISEKI archive API v0.0.1"}


@app.get("/works/<work_id>")
def get_work(work_id: str) -> Response:
    work = wnss.get_work(work_id)
    if work is None:
        status_code = 404
        body = {"message": "works not found"}
    else:
        cms_endpoint = WnssEndpoint()
        cms = cms_endpoint.get_contents(work["cms_id"])

        status_code = 200
        body = {**work, **cms}
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(body, default=json_serial),
    )


def lambda_handler(event: dict, context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
