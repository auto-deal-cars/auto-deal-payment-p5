"""Module responsible for handling exceptions in the application."""
from functools import wraps
import json
from logging import Logger
from typing import Callable
from pydantic import ValidationError

from payment.exceptions.custom_exception import PaymentCustomException

def event_exception_handler(logger: Logger):
    """Decorator responsible for handling HTTP exceptions in the controller."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as error:
                logger.error(f"Validation error: {error.errors(include_url=False)}")
            except PaymentCustomException as exception:
                logger.error(f"Payment custom exception: {exception.message}")
            except KeyError as error:
                logger.error(f"Key error: {str(error)}")
            except ValueError as error:
                logger.error(f"Value error: {str(error)}")
            except Exception as exception:
                logger.error(f"An unexpected error occurred: {str(exception)}")

        return wrapper
    return decorator

def http_exception_handler(func: Callable):
    """Decorator responsible for handling HTTP exceptions in the controller."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as error:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Validation error',
                    'errors': error.errors(include_url=False)
                })
            }
        except PaymentCustomException as exception:
            return {
                'statusCode': exception.status_code,
                'body': json.dumps({
                    'message': exception.message
                })
            }
        except KeyError as error:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Key error',
                    'error': str(error)
                })
            }
        except ValueError:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Key error',
                    'error': str(error)
                })
            }
        except Exception as exception:
            print(exception)
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'An error occurred',
                })
            }

    return wrapper
