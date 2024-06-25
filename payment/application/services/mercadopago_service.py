"""
This module contains the implementation of the Mercado Pago service.
"""
import os
import mercadopago

class MercadopagoService:
    """
    This class implements the Mercado Pago service.
    """
    def __init__(self) -> None:
        self.default_cpf = "12345678909"
        self.sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

    def pay(self, vehicle_id: str, idempotency_key: str):
        """
        This method prepares the data for the payment.
        """
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            "x-idempotency-key": idempotency_key
        }

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
                    "number": self.default_cpf
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

        return self.create_new_payment(payment_data, request_options)

    def create_new_payment(self, payment_data: dict, request_options: dict):
        """
        This method creates a new payment.
        """
        payment_response = self.sdk.payment().create(payment_data, request_options)
        payment = payment_response["response"]

        return payment
