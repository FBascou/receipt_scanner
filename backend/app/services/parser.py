from datetime import datetime
import re
from typing import List

total_keywords = ["totale complessivo", "totale euro", "totale"]

def extract_total(text: str) -> float:
    """
    Find the total amount from OCR text by checking if the previous word is in total_keywords.
    """
    text = text.upper().replace("\n", " ")
    
    matches: List[float] = []

    for keyword in total_keywords:
        pattern = rf"{keyword}\s*([\d]+(?:[.,][\d]+)?)"

        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                value = float(match.group(1).replace(",", "."))
                matches.append(value)
            except ValueError:
                continue

    return max(matches) if matches else 0.0

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