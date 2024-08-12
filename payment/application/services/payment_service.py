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
cognito = boto3.client("cognito-idp")
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

    def get_user_info(self, access_token: str):
        """
        This method retrieves the user info from the access token.
        """

        user_data = cognito.get_user(AccessToken=access_token)
        return user_data.get("UserAttributes")

    def start_payment(
            self,
            idempotency_key: str,
            vehicle_id: int,
            access_token: str
        ) -> dict:
        """
        This method starts a PIX payment.
        """
        user_info = self.get_user_info(access_token)
        user_dict = {item['Name']: item['Value'] for item in user_info}

        email = user_dict.get('email', {})
        user_details = json.loads(user_dict.get('custom:user_details', {}))
        address = json.loads(user_dict.get('custom:address', {}))

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            "x-idempotency-key": idempotency_key
        }

        payment_data = {
            "transaction_amount": 1,
            "description": f"Vehicle {vehicle_id}",
            "payment_method_id": "pix",
            "payer": {
                "email": email,
                "first_name": user_details.get("first_name", {}),
                "last_name": user_details.get("last_name", {}),
                "identification": {
                    "type": "CPF",
                    "number": user_details.get("cpf", {})
                },
                "address": {
                    "zip_code": address.get("zip_code", {}),
                    "street_name": address.get("street_name", {}),
                    "street_number": address.get("street_number", {}),
                    "neighborhood": address.get("neighborhood", {}),
                    "city": address.get("city", {}),
                    "federal_unit": address.get("federal_unit", {})
                    }
                }
        }

        payment_response = self.sdk.payment().create(payment_data, request_options)
        payment_response = payment_response["response"]

        return payment_response
