from PIL import Image
import pytesseract
from io import BytesIO

async def parseImage(file: BytesIO):
    """
        Method Name: parseImage
        Description: This method extracts text from an image file using Tesseract OCR. It reads the image
                     and returns the detected text as a string.
        Input: BytesIO file (Image file in memory)
        Output: Extracted text from the image as a string
        On Failure: Raises RuntimeError with error message

        Written By: Aman, Sonika
        Version: 1.0
    """
    try:
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    except Exception as e:
        raise RuntimeError(f"Image parsing failed: {str(e)}")