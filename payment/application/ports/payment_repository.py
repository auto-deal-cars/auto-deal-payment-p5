"""
This module contains the definition of the PaymentRepository interface.
"""
from abc import ABC, abstractmethod

class PaymentRepository(ABC):
    """
    This interface defines the methods that a payment repository must implement.
    """
    @abstractmethod
    def create(self, payment: dict):
        """
        This method creates a new payment.
        """
        pass

    @abstractmethod
    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        This method retrieves a payment by its idempotency key.
        """
        pass

    @abstractmethod
    def transform_payment_to_prettified_response(self, payment: dict) -> dict:
        """
        This method transforms a payment to a prettified dictionary response.
        """
        pass

    def store_payment(self, payment: dict):
        """
        This method stores a payment.
        """
        pass
