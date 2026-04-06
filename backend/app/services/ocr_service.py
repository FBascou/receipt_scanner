import io
from PIL import Image
from app.services.ocr_engine import extract_text
from app.services.parser import extract_date, extract_total
from app.schemas.receipt import ReceiptCreate
    
def process_image(image_bytes: bytes) -> ReceiptCreate:
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")

    extracted_text = extract_text(image)

    return ReceiptCreate(
        total_amount=extract_total(extracted_text),
        date=extract_date(extracted_text),
        raw_text=extracted_text,
    )