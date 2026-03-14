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

# REGISTER
class EmailAlreadyRegistered(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=EMAIL_ALREADY_REGISTERED,
            message="Email already registered, please try a different one",
            field="email",
        ) 
        
class PasswordTooShort(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=PASSWORD_TOO_SHORT,
            message="Password should have a minimum of 8 characters",
            field="password",
        ) 
 
class PasswordNotValid(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=PASSWORD_NOT_VALID,
            message="Password should have at least one uppercase English letter, one lowercase English letter, one number, and one special character (#, ?, !, @, $, %, ^, &, *, -)",
            field="password",
        ) 
     
# LOGIN     
class InvalidCredentials(APIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=INVALID_CREDENTIALS,
            message="Invalid email or password",
        )

class Forbidden(APIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            code=FORBIDDEN,
            message="You are not allowed to access this resource",
        )

class UserNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=USER_NOT_FOUND,
            message="User not found",
            field="user_id",
        )

class JobNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=JOB_NOT_FOUND,
            message="Job not found",
            field="job_id",
        )