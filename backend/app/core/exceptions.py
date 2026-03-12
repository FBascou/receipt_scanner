from fastapi import HTTPException
from typing import Optional, Dict, Any
from .error_codes import *

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field: Optional[str] = None,
    ):
        detail: Dict[str, Any] = {
            "error": {
                "code": code,
                "message": message,
                "field": field,
                "status": status_code,
            }
        }
        super().__init__(status_code=status_code, detail=detail)
        
class InvalidCredentials(APIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=INVALID_CREDENTIALS,
            message="Invalid email or password",
        )

class UserNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=USER_NOT_FOUND,
            message="User not found",
            field="user_id",
        )

class EmailAlreadyRegistered(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=EMAIL_ALREADY_REGISTERED,
            message="Email already registered",
            field="email",
        )

class JobNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=JOB_NOT_FOUND,
            message="Job not found",
            field="job_id",
        )

class Forbidden(APIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            code=FORBIDDEN,
            message="You are not allowed to access this resource",
        )