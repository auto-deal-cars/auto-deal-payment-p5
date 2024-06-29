"""
Get payment from DynamoDB
"""
import json

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService

def get_payment(event, context):
    """
    Get payment from DynamoDB
    """
    body = json.loads(event["body"])
    idempotency_key = body["idempotency_key"]

    payment_repository = DynamoDBPaymentRepository()
    payment_service = PaymentService(payment_repository)
    payment_response = payment_service.get_payment_by_idempotency_key(
        idempotency_key,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(payment_response)
    }
