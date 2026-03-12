from datetime import datetime
import re

def extract_total(text: str) -> float:
    """
    Extract the most likely total amount from OCR text.
    """
    # Match prices like 12.34 but avoid years (20xx)
    candidates = re.findall(
        r'(?<!\d)(\d{1,4}\.\d{2})(?!\d)',
        text
    )

    values: list[float] = []

    for c in candidates:
        value = float(c)
        # Filter out years or nonsense values
        if 0 < value < 10000:
            values.append(value)

    if not values:
        return 0.0

    return max(values)

def extract_date(text: str) -> str:
    """
    Extract date from receipt text.
    """
    patterns = [
        r'\b\d{2}[./-]\d{2}[./-]\d{4}\b',  # 31/12/2024, 31.12.2024
        r'\b\d{4}[./-]\d{2}[./-]\d{2}\b',  # 2024-12-31
        r'\b\d{2}[./-]\d{4}\b',            # 31.2026
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return "unknown"

def sanitize_ocr_date(ocr_date: str) -> str:
    """
    Convert OCR date into YYYY-MM-DD format. If parsing fails, return 'unknown'.
    """
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(ocr_date, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return "unknown"