import ipaddress

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from .error_codes import INTERNAL_SERVER_ERROR, VALIDATION_ERROR
import re

# FastAPI default validation response:
# {
#  "detail": [...]
# }
# This breaks your frontend contract.
# We want all errors to look identical.
# So we override with validation_exception_handler 
# validation errors match the error schema.

async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    # Ensure it is actually a validation error
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": VALIDATION_ERROR,
                    "message": "Invalid request",
                    "field": None,
                    "status": 422,
                }
            },
        )

    # Fallback 
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": INTERNAL_SERVER_ERROR,
                "message": "Unexpected error",
                "field": None,
                "status": 500,
            }
        },
    )
    

def verify_device_mac(mac: str) -> bool:
    # regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    # regex = r'^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$'
    regex = r'^([0-9A-Fa-f]{2})([:-])(?:[0-9A-Fa-f]{2}\2){4}[0-9A-Fa-f]{2}$'
    validate = re.compile(regex)
    return bool(validate.match(mac))

def verify_device_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False