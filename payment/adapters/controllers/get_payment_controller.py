"""
Get payment from DynamoDB
"""
import json
import os
import mercadopago

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService

sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

def get_payment(event, context):
    """
    Get payment from DynamoDB
    """
    body = json.loads(event["body"])
    idempotency_key = body["idempotency_key"]

    payment_repository = DynamoDBPaymentRepository()
    payment_service = PaymentService(payment_repository)

    response = payment_repository.get_payment_by_idempotency_key(idempotency_key)
    item = response["Item"]
    prettified_response = payment_service.pretty_print_payment(item)

    return {
        "statusCode": 200,
        "body": json.dumps(prettified_response)
    }
