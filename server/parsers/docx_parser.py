from docx import Document
from io import BytesIO

async def parseDocs(file: BytesIO):
    """
        Method Name: parseDocs
        Description: This method extracts text from a DOCX file using python-docx. It reads all the
                     paragraphs and combines them into a single string with newlines.
        Input: BytesIO file (DOCX file in memory)
        Output: Extracted text as a string
        On Failure: Raises RuntimeError with error message

        Written By: Aman, Sonika
        Version: 1.0
    """
    try:
        doc = Document(file)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise RuntimeError(f"Docx parsing failed: {str(e)}")
    