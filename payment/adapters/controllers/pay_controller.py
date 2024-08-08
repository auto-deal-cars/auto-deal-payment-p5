"""Payment controller"""
import json
import logging

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService
from payment.domain.payment import Payment as PaymentEntity
from payment.exceptions.custom_orm_exceptions import handle_custom_exceptions
from payment.exceptions.exception_handler import event_exception_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@event_exception_handler(logger)
@handle_custom_exceptions
def create_payment(event, context):
    """Payment controller"""
    body = json.loads(event["Records"][0]["body"])
    vehicle_id = body["vehicle_id"]
    order_id = body["order_id"]
    idempotency_key = body["idempotency_key"]
    access_token = body["access_token"]

    payment_repository = DynamoDBPaymentRepository()
    payment_service = PaymentService(payment_repository)
    payment = payment_service.start_payment(
        idempotency_key,
        vehicle_id,
        access_token
    )

    payment_entity = PaymentEntity(
        idempotency_key=idempotency_key,
        order_id=order_id,
        vehicle_id=vehicle_id,
        payment_id=payment["id"],
        status=payment["status"],
    )

    payment_service.create_payment(payment_entity)

    logging.info(f"Payment started with {idempotency_key} and order {order_id}")
