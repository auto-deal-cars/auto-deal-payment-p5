"""
Get payment from Mercado Pago
"""
import os
import json
import boto3
import mercadopago

sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

def get_payment(event, context):
    """
    Get payment from Mercado Pago
    """
    body = json.loads(event["body"])
    idempotency_key = body["idempotency_key"]
    client = boto3.client("dynamodb")

    response = client.get_item(
        TableName=f"{os.environ.get('TABLE_NAME')}-dev",
        Key={
            "idempotency_key": {"S": idempotency_key}
        }
    )
    item = response["Item"]

    prettified_response = {
        "idempotency_key": item["idempotency_key"]["S"],
        "payment_id": item["payment_id"]["N"],
        "status": item["status"]["S"],
        "order_id": item["order_id"]["N"],
        "external_id": item["external_id"]["N"],
        "vehicle_id": item["vehicle_id"]["N"],
        "created_at": item["created_at"]["S"],
        "updated_at": item["updated_at"]["S"],
    }

    return {
        "statusCode": 200,
        "body": json.dumps(prettified_response)
    }
