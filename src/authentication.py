from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
import firebase_admin
from firebase_admin import credentials, auth

from aws_client.parameter_store import get_parameter


init = False


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    effect = 'Deny'

    global init
    if not init:
        charge = {
            "type": "service_account",
            "project_id": get_parameter("FIREBASE_PROJECT_ID"),
            "private_key_id": get_parameter("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": get_parameter("FIREBASE_PRIVATE_KEY"),
            "client_email": get_parameter("FIREBASE_CLIENT_EMAIL"),
            "client_id": get_parameter("FIREBASE_CLIENT_ID"),
            "auth_uri": get_parameter("FIREBASE_AUTH_URI"),
            "token_uri": get_parameter("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": get_parameter("FIREBASE_AUTH_X509_CERT_URI"),
            "client_x509_cert_url": get_parameter("FIREBASE_CLIENT_X509_CERT_URI"),
            "universe_domain": "googleapis.com",
        }
        charge["private_key"] = charge["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(charge)
        firebase_admin.initialize_app(cred)
        init = True

    decoded_token = auth.verify_id_token(event["authorizationToken"])
    uid = decoded_token['uid']

    if uid:
        effect = 'Allow'

    return {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': event['methodArn']
            }]
        },
        'context': {
            'uid': uid,
        }
    }
