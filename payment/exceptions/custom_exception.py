"""Handled exception class for handling errors in the user module."""

class PaymentCustomException(Exception):
    """Handled exception class for handling errors in the payment module."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
