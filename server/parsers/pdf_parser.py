import pdfplumber
import pytesseract
from PIL import Image
from io import BytesIO

async def parsePdf(file: BytesIO):
    """
        Method Name: parsePdf
        Description: This method extracts text from a PDF file. It first tries normal text extraction using
                     pdfplumber, and if it fails, it uses OCR (Tesseract) as a fallback to get the content.
        Input: BytesIO file (PDF file in memory)
        Output: Extracted text from the resume as a string
        On Failure: Raises RuntimeError with error message

        Written By: Aman, Sonika
        Version: 1.0
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                pageText = page.extract_text()
                text += f"{pageText}\n" if pageText else ""
        #if pdf fails then will use OCR
        if not text.strip():
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    img = page.to_image()
                    img.save("temp_page.png")
                    text += pytesseract.image_to_string(Image.open("temp_page.png"))+"\n"
    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {str(e)}")
    return text