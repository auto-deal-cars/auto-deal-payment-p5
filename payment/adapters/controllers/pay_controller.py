"""Payment controller"""
import json

from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository
from payment.application.services.payment_service import PaymentService

def create_payment(event, context):
    """Payment controller"""
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
