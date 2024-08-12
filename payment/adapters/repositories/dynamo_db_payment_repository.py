"""
This module contains the implementation of the DynamoDB payment repository.
"""
import os
from datetime import datetime
import boto3

from payment.application.ports.payment_repository import PaymentRepository
from payment.domain.payment import Payment

class DynamoDBPaymentRepository(PaymentRepository):
    """
    This class implements the DynamoDB payment repository.
    """
    def __init__(self):
        """
        This method initializes the DynamoDB payment repository.
        """
        self.client = boto3.client("dynamodb")
        self.table_name = f"{os.environ.get('TABLE_NAME')}"

    def create(self, payment: Payment):
        """
        This method creates a new payment.
        """
        self.client.put_item(
            TableName=self.table_name,
            Item={
                "idempotency_key": {"S": payment.idempotency_key},
                "status": {"S": payment.status},
                "order_id": {"N": str(payment.order_id)},
                "payment_id": {"N": str(payment.payment_id)},
                "vehicle_id": {"N": str(payment.vehicle_id)},
                "created_at": {"S": datetime.now().isoformat()},
                "updated_at": {"S": datetime.now().isoformat()}
            }
        )

    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        This method retrieves a payment by its idempotency key.
        """
        response = self.client.scan(
            TableName=self.table_name,
            FilterExpression="idempotency_key = :idempotency_key",
            ExpressionAttributeValues={
                ":idempotency_key": {"S": idempotency_key}
            }
        )

        item = response["Items"][0]

        return self.transform_payment_to_prettified_response(item)

    def get_payment_by_payment_id(self, payment_id: int) -> dict:
        """
        This method retrieves a payment by its payment id.
        """
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                "payment_id": {"N": str(payment_id)}
            }
        )
        item = response["Item"]

        return self.transform_payment_to_prettified_response(item)

    def transform_payment_to_prettified_response(self, payment: dict) -> dict:
        """
        This method transforms a payment to a prettified dictionary response.
        """
        prettified_response = {
            "idempotency_key": payment["idempotency_key"]["S"],
            "payment_id": payment["payment_id"]["N"],
            "status": payment["status"]["S"],
            "order_id": payment["order_id"]["N"],
            "vehicle_id": payment["vehicle_id"]["N"],
            "created_at": payment["created_at"]["S"],
            "updated_at": payment["updated_at"]["S"],
        }

        return prettified_response

    def update_payment(self, payment_id: str, status: str):
        """
        This method updates a payment.
        """
        self.client.update_item(
            TableName=self.table_name,
            Key={
                "payment_id": {"N": payment_id}
            },
            UpdateExpression="set #status = :status, updated_at = :updated_at",
            ExpressionAttributeNames={
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":status": {"S": status},
                ":updated_at": {"S": datetime.now().isoformat()}
            }
        )
