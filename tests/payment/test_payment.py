"""Test payment domain model"""
import pytest
from payment.domain.payment import Payment

@pytest.fixture
def payment() -> Payment:
    """Payment fixture"""
    return Payment(
        idempotency_key="123",
        status="pending",
        order_id=123,
        payment_id=123,
        vehicle_id=123,
        created_at="2021-01-01",
        updated_at="2021-01-01",
    )

def test_payment_model(payment: Payment):
    """Test payment model"""
    assert payment.idempotency_key == "123"
    assert payment.status == "pending"
    assert payment.order_id == 123
    assert payment.payment_id == 123
    assert payment.vehicle_id == 123
    assert payment.created_at == "2021-01-01"
    assert payment.updated_at == "2021-01-01"

def test_payment_with_invalid_idempotency_key():
    """Test payment with invalid idempotency key"""
    with pytest.raises(ValueError):
        Payment(idempotency_key="")

def test_payment_with_invalid_status():
    """Test payment with invalid status"""
    with pytest.raises(ValueError):
        Payment(status="")

def test_payment_with_invalid_order_id():
    """Test payment with invalid order id"""
    with pytest.raises(ValueError):
        Payment(order_id="")

def test_payment_with_invalid_payment_id():
    """Test payment with invalid payment id"""
    with pytest.raises(ValueError):
        Payment(payment_id="")

def test_payment_with_invalid_vehicle_id():
    """Test payment with invalid vehicle id"""
    with pytest.raises(ValueError):
        Payment(vehicle_id="")
