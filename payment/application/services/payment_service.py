"""
This module contains the implementation of the payment service.
"""
from payment.application.ports.payment_repository import PaymentRepository

class PaymentService:
    """
    This class implements the payment service.
    """
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def create_payment(self, payment: dict):
        """
        This method creates a new payment.
        """
        return self.payment_repository.create(payment)

    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        This method retrieves a payment by its idempotency key.
        """
        return self.payment_repository.get_payment_by_idempotency_key(idempotency_key)
