"""Custom exceptions."""

from functools import wraps
from typing import Callable
from aws_error_utils import errors
from payment.exceptions.custom_exception import PaymentCustomException

def handle_custom_exceptions(func: Callable):
    """Decorator to handle custom exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.ClientError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Client error',
            ) from exception
        except errors.EndpointConnectionError as exception:
            raise PaymentCustomException(
                status_code=503,
                message='Endpoint connection error',
            ) from exception
        except errors.NoCredentialsError as exception:
            raise PaymentCustomException(
                status_code=401,
                message='No valid credentials provided',
            ) from exception
        except errors.PartialCredentialsError as exception:
            raise PaymentCustomException(
                status_code=401,
                message='Partial credentials provided',
            ) from exception
        except errors.ParamValidationError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Parameter validation error',
            ) from exception
        except errors.IncompleteSignatureError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Incomplete signature error',
            ) from exception
        except errors.SSLError as exception:
            raise PaymentCustomException(
                status_code=500,
                message='SSL error',
            ) from exception
        except errors.ConnectionClosedError as exception:
            raise PaymentCustomException(
                status_code=503,
                message='Connection closed unexpectedly',
            ) from exception
        except errors.WaiterError as exception:
            raise PaymentCustomException(
                status_code=500,
                message='Waiter error',
            ) from exception
        except errors.DataNotFoundError as exception:
            raise PaymentCustomException(
                status_code=404,
                message='Data not found',
            ) from exception
        except errors.UnknownServiceError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Unknown service error',
            ) from exception
        except errors.InvalidRegionError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Invalid region specified',
            ) from exception
        except errors.ProfileNotFound as exception:
            raise PaymentCustomException(
                status_code=404,
                message='Profile not found',
            ) from exception
        except errors.ConfigNotFound as exception:
            raise PaymentCustomException(
                status_code=404,
                message='Configuration file not found',
            ) from exception
        except errors.InvalidConfigError as exception:
            raise PaymentCustomException(
                status_code=400,
                message='Invalid configuration',
            ) from exception
        except Exception as exception:
            raise PaymentCustomException(
                status_code=500,
                message='Internal server error',
            ) from exception

    return wrapper
