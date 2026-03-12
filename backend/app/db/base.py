from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they are registered with Base
from app.db.models import User, Receipt, ReceiptJob  # type: ignore # noqa