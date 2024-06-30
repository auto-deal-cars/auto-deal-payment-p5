"""Payment controller"""
import json
import logging
from pydantic import ValidationError

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def create_payment(event, context):
    """Payment controller"""
    logger.info("Starting payment")
    try:
        body = json.loads(event["Records"][0]["body"])
        vehicle_id = body["vehicle_id"]
        order_id = body["order_id"]
        idempotency_key = body["idempotency_key"]

        payment_repository = DynamoDBPaymentRepository()
        payment_service = PaymentService(payment_repository)
        payment = payment_service.start_payment(idempotency_key, vehicle_id)

        payment_service.create_payment({
            **payment,
            "idempotency_key": idempotency_key,
            "order_id": order_id,
            "vehicle_id": vehicle_id
        })

        logging.info(f"Payment started with {idempotency_key} and order {order_id}")

    except ValidationError as e:
        logger.error(f"Validation error: {e}")

    except Exception as e:
        logger.error(f"Error: {e}")
