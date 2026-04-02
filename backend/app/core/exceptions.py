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

# GENERIC 
class Forbidden(APIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            code=FORBIDDEN,
            message="You are not allowed to access this resource",
        )

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
            code=PASSWORD_INVALID,
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

class UserNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=USER_NOT_FOUND,
            message="User not found",
            field="user_id",
        )

# DEVICES 
class DeviceNotFound(APIException): 
    def __init__(self):
        super().__init__(
            status_code=404,
            code=DEVICE_NOT_FOUND,
            message="Device not found",
            field="device_id",
        )

class DeviceInvalid(APIException): 
    def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_INVALID,
            message="Device not valid",
            field="device_id",
        )

class DeviceInvalidName(APIException): 
    def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_INVALID_NAME,
            message="Device name not valid",
            field="name", 
        )
        
class DeviceInvalidMac(APIException): 
    def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_INVALID_MAC,
            message="Device mac address not valid",
            field="mac",
        )

class DeviceInvalidIp(APIException): 
    def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_INVALID_IP,
            message="Device IP not valid",
            field="ip",
        )

class DeviceAlreadyRegistered(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_ALREADY_REGISTERED,
            message="Device already registered, please try a different one",
            field="device_id",
        ) 

# JOBS
class JobNotFound(APIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code=JOB_NOT_FOUND,
            message="Job not found",
            field="job_id",
        )

class JobInvalidId(APIException): 
    def __init__(self):
        super().__init__(
            status_code=400,
            code=JOB_INVALID_ID,
            message="Job ID not valid",
            field="job_id",
        )        
        
# RECEIPTS
class DeviceRequired(APIException):
     def __init__(self):
        super().__init__(
            status_code=400,
            code=DEVICE_REQUIRED,
            message="Device required for automatic jobs",
            field="source",
        )