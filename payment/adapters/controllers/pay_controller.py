"""Payment controller"""
import os
import json
from datetime import datetime
import boto3
import mercadopago

sdk = mercadopago.SDK(os.environ.get("ENV_ACCESS_TOKEN"))

def create_payment(event, context):
    """Payment controller"""

    body = json.loads(event["Records"][0]["body"])
    vehicle_id = body["vehicle_id"]
    order_id = body["order_id"]
    idempotency_key = body["idempotency_key"]

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

    payment_response = sdk.payment().create(payment_data, request_options)
    payment = payment_response["response"]
    client = boto3.client("dynamodb")

    try:
        client.put_item(
            TableName=f"{os.environ.get('TABLE_NAME')}-dev",
            Item={
                "idempotency_key": {"S": str(idempotency_key)},
                "status": {"S": payment["status"]},
                "order_id": {"N": str(order_id)},
                "payment_id": {"N": str(payment["id"])},
                "external_id": {"N": str(payment["id"])},
                "vehicle_id": {"N": str(vehicle_id)},
                "created_at": {"S": datetime.now().isoformat()},
                "updated_at": {"S": datetime.now().isoformat()}
            }
        )
    except Exception as error:
        print("Error saving payment to dynamodb", error)

    return {
        "statusCode": 201,
        "body": json.dumps(payment)
    }
