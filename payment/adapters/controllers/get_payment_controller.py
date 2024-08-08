"""
Get payment from DynamoDB
"""
import json
import os
import logging
import mercadopago

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService
from payment.exceptions.custom_orm_exceptions import handle_custom_exceptions
from payment.exceptions.exception_handler import http_exception_handler

sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@http_exception_handler
@handle_custom_exceptions
def get_payment(event, context):
    """
    Get payment from DynamoDB
    """
    logger.info("Getting payment")
    body = json.loads(event["body"])
    idempotency_key = body["idempotency_key"]

    payment_repository = DynamoDBPaymentRepository()
    payment_service = PaymentService(payment_repository)

    response = payment_service.get_payment_by_idempotency_key(idempotency_key)

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
