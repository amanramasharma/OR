from .pdf_parser import parsePdf
from .docx_parser import parseDocs
from .image_parser import parseImage

from io import BytesIO

async def parseResume(file):
    """
        Method Name: parseResume
        Description: Detects file format and routes it to the appropriate parser (PDF, DOCX, Image).
        Input: UploadFile (from FastAPI)
        Output: Extracted text string
        On Failure: Raises ValueError for unsupported formats

        Written By: Aman, Sonika
        Version: 1.0
    """
    filename = file.filename.lower()
    content = await file.read()
    file_bytes = BytesIO(content)

    if filename.endswith(".pdf"):
        return await parsePdf(file_bytes)
    elif filename.endswith(".docx"):
        return await parseDocs(file_bytes)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return await parseImage(file_bytes)
    else:
        raise ValueError("Unsupported file format.")