"""
This module contains the implementation of the payment service.
"""
import json
import os
import boto3
import mercadopago
import requests
from payment.application.ports.payment_repository import PaymentRepository
from payment.domain.payment import Payment

sqs = boto3.client("sqs")
class PaymentService:
    """
    This class implements the payment service.
    """
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository
        self.sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

    def create_payment(self, payment: Payment):
        """
        This method creates a new payment.
        """
        return self.payment_repository.create(payment)

    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        This method retrieves a payment by its idempotency key.
        """
        return self.payment_repository.get_payment_by_idempotency_key(idempotency_key)

    def get_payment_by_id_from_source(self, payment_id: str) -> dict:
        """
        This method retrieves a payment by its id from the source.
        """
        url = f"{os.environ['MERCADO_PAGO_API_URL']}{payment_id}"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {os.environ['ENV_ACCESS_TOKEN']}"},
            timeout=15
        )

        return response.json()

    def handle_success_payment(self, payment_id: int):
        """
        This method handles a successful payment.
        """
        payment = self.payment_repository.get_payment_by_payment_id(payment_id)
        sqs.send_message(
            QueueUrl=os.environ['SUCCESS_PAYMENT_QUEUE_URL'],
            MessageBody=json.dumps({
                "payment_id": payment["payment_id"],
                "vehicle_id": payment["vehicle_id"],
            })
        )

        self.payment_repository.update_payment(
            payment_id=payment_id,
            status='success'
        )

    def handle_failed_payment(self, payment_id: str):
        """
        This method handles a failed payment.
        """
        payment = self.payment_repository.get_payment_by_payment_id(payment_id)
        sqs.send_message(
            QueueUrl=os.environ['FAILED_PAYMENT_QUEUE_URL'],
            MessageBody=json.dumps({
                "payment_id": payment["payment_id"],
                "vehicle_id": payment["vehicle_id"],
            })
        )

        self.payment_repository.update_payment(
            payment_id=payment_id,
            status='failed'
        )

    def start_payment(self, idempotency_key: str, vehicle_id: int):
        """
        This method starts a PIX payment.
        """
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            "x-idempotency-key": idempotency_key
        }
        default_cpf = "12345678909"

        payment_data = {
            "transaction_amount": 1,
            "description": f"Vehicle {vehicle_id}",
            "payment_method_id": "pix",
            "payer": {
                "email": os.environ.get("DEFAULT_EMAIL"),
                "first_name": "John",
                "last_name": "Doe",
                "identification": {
                    "type": "CPF",
                    "number": default_cpf
                },
                "address": {
                    "zip_code": os.environ.get("ZIP_CODE"),
                    "street_name": os.environ.get("STREET_NAME"),
                    "street_number": os.environ.get("STREET_NUMBER"),
                    "neighborhood": os.environ.get("NEIGHBORHOOD"),
                    "city": os.environ.get("CITY"),
                    "federal_unit": os.environ.get("FEDERAL_UNIT")
                }
            }
        }

        payment_response = self.sdk.payment().create(payment_data, request_options)
        payment_response = payment_response["response"]

        return payment_response
