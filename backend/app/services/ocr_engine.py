from typing import cast
import numpy as np
import cv2
from PIL import Image
import pytesseract # pyright: ignore[reportMissingTypeStubs]

# Function created to isolate pytesseract.image_to_string(image) because it returns error  Type of "image_to_string" is partially unknown
def _image_to_string(image: np.ndarray) -> str:
    return cast(str, pytesseract.image_to_string(image)) # type: ignore[reportUnknownMemberType]

def extract_text(image: Image.Image) -> str:
    # Convert PIL Image to numpy array
    img = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return _image_to_string(thresh)