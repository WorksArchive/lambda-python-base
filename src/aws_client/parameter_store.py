import requests
import os
from typeguard import typechecked


@typechecked
def get_parameter(parameter_name: str) -> str:
    value = ""
    end_point = "http://localhost:2773"
    path = (
        "/systemsmanager/parameters/get/?name="
        + parameter_name
        + "&withDecryption=true"
    )
    url = end_point + path
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ["AWS_SESSION_TOKEN"]}

    res = requests.get(url, headers=headers)
    if res.ok:
        value = res.json()["Parameter"]["Value"]

    return value
