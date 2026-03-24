from enum import Enum

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class JobUploadSource(str, Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"