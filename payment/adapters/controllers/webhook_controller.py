"""
This module is used to notify the payment service that a payment has been made.
"""
import logging
from typing import Final
from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

PAYMENT_UPDATED_EVENT: Final[str] = 'payment.updated'
PAYMENT_STATUS_APPROVED: Final[str] = 'approved'

def webhook_notify(event, context):
    """
    This method is used to notify the payment service that a payment has been made.
    """
    logging.info(f"Received event: {event}")
    try:
        action = event['body']['action']
        payment_id = event['body']['data']['id']

        payment_repository = DynamoDBPaymentRepository()
        payment_service = PaymentService(payment_repository)

        if action != PAYMENT_UPDATED_EVENT:
            logging.info("Webhook payment failed")
            payment_service.handle_failed_payment(
                payment_id=payment_id
            )
            return {
                'statusCode': 200
            }

        if action == PAYMENT_UPDATED_EVENT:
            response = payment_service.get_payment_by_id_from_source(payment_id)

        if response['status'] == PAYMENT_STATUS_APPROVED:
            logging.info("Webhook payment success")
            payment_service.handle_success_payment(
                payment_id=payment_id
            )

            return {
                'statusCode': 200
            }

        payment_service.handle_failed_payment(
            payment_id=payment_id
        )
    except Exception as e:
        logging.error(f"Error: {e}")

        return {
            'statusCode': 500
        }

    logging.info("Webhook processed with 404 status code")

    return {
        'statusCode': 404
    }
