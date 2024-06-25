"""Payment controller"""
import json

from payment.application.services.mercadopago_service import MercadopagoService
from payment.adapters.repositories.dynamo_db_payment_repository import DynamoDBPaymentRepository

def create_payment(event, context):
    """Payment controller"""
    body = json.loads(event["Records"][0]["body"])
    vehicle_id = body["vehicle_id"]
    order_id = body["order_id"]
    idempotency_key = body["idempotency_key"]

    mercadopago_service = MercadopagoService()
    payment_repository = DynamoDBPaymentRepository()
    payment = mercadopago_service.pay(vehicle_id, idempotency_key)

    try:
        payment_repository.store_payment({
            "idempotency_key": idempotency_key,
            "status": payment["status"],
            "order_id": order_id,
            "payment_id": payment["id"],
            "external_id": payment["id"],
            "vehicle_id": vehicle_id
        })
    except Exception as error:
        print("Error saving payment to dynamodb", error)
