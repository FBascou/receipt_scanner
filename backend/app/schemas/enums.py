from enum import Enum

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class JobSource(str, Enum):
    MANUAL = "manual_upload"
    AUTOMATIC = "automatic_upload"