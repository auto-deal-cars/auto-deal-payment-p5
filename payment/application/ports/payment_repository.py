"""
PaymentRepository is an interface that defines the methods that a payment repository must implement.
"""
from abc import ABC, abstractmethod

class PaymentRepository(ABC):
    """
    PaymentRepository is an interface.
    """
    @abstractmethod
    def create(self, payment: dict) -> None:
        """
        Create a payment in the repository.
        """
        pass

    @abstractmethod
    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        Get a payment from the repository by idempotency key.
        """
        pass

    @abstractmethod
    def get_payment_by_payment_id(self, payment_id: int) -> dict:
        """
        Get a payment from the repository by payment id.
        """
        pass

    @abstractmethod
    def transform_payment_to_prettified_response(self, payment: dict) -> dict:
        """
        Transform a payment to a prettified response.
        """
        pass


    @abstractmethod
    def update_payment(self, payment_id: str, status: str) -> None:
        """
        Update a payment in the repository.
        """
        pass
