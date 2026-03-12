import io
from typing import List
from PIL import Image

# TODO:
# Add logging middleware
# Add background job queue
# Improve OCR extraction reliability
# Convert date from str → real date
# Add confidence scoring for OCR
# Add strict mode for job validation
# Add automatic currency extraction normalization
# Make the JSON export fully typed using a dedicated export schema
# Or show how to eliminate Any completely using TypedDict
# Or review the entire project structure one more time for production-readiness


# def generate_pdf_from_images(images: list[Image.Image]) -> bytes:
#     if not images:
#         raise ValueError("No images")

#     buffer = io.BytesIO()

#     first = images[0]
#     rest = images[1:]

#     first.save(
#         buffer,
#         format="PDF",
#         save_all=True,
#         append_images=rest,
#     )

#     buffer.seek(0)
#     return buffer.read()

def generate_pdf_from_images(images: List[Image.Image]) -> bytes:
    """
    Convert a list of PIL Images into a single PDF bytes object.
    """
    if not images:
        raise ValueError("No images to generate PDF")

    pdf_bytes_io = io.BytesIO()
    first, *rest = images
    first.save(pdf_bytes_io, format="PDF", save_all=True, append_images=rest)
    pdf_bytes_io.seek(0)
    return pdf_bytes_io.read()