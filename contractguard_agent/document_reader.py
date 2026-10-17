from pathlib import Path
import re

import pymupdf
import pytesseract
from PIL import Image
from pypdf import PdfReader
from docx import Document


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================
# OCR TEXT CLEANING
# ============================================================

def clean_ocr_text(text: str) -> str:
    """
    Clean common OCR mistakes.

    Examples:
        6@ days  -> 60 days
        5@,0@@   -> 50,000
    """

    def replace_ocr_zero(match):
        token = match.group(0)

        if any(char.isdigit() for char in token):
            return token.replace("@", "0")

        return token

    cleaned_text = re.sub(
        r"\d[\d@,]*",
        replace_ocr_zero,
        text
    )

    return cleaned_text


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(path: Path) -> str:
    """
    Extract text from a normal text-based PDF.
    """

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text and text.strip():
            pages.append(text)

    return "\n".join(pages).strip()


# ============================================================
# PDF OCR
# ============================================================

def extract_pdf_with_ocr(path: Path) -> str:
    """
    Extract text from scanned/image-based PDF using
    PyMuPDF + Tesseract OCR.
    """

    try:
        pdf_document = pymupdf.open(str(path))

        ocr_pages = []

        for page_number, page in enumerate(pdf_document, start=1):

            # Render page at 2x resolution
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False
            )

            # Convert rendered page to PIL image
            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # OCR
            text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            if text and text.strip():
                ocr_pages.append(text)

        pdf_document.close()

        extracted_text = "\n".join(ocr_pages).strip()

        if not extracted_text:
            return "Error reading PDF: OCR could not extract any text."

        # Clean common OCR mistakes
        extracted_text = clean_ocr_text(extracted_text)

        return extracted_text

    except Exception as e:
        return f"Error reading PDF with OCR: {str(e)}"


# ============================================================
# PDF READER
# ============================================================

def read_pdf(path: Path) -> str:
    """
    Read a PDF.

    First:
        Try normal text extraction.

    If no text is found:
        Automatically use OCR.
    """

    try:

        # ----------------------------------------------------
        # STEP 1: Normal PDF extraction
        # ----------------------------------------------------

        extracted_text = extract_pdf_text(path)

        if extracted_text:
            return extracted_text

        # ----------------------------------------------------
        # STEP 2: OCR fallback
        # ----------------------------------------------------

        return extract_pdf_with_ocr(path)

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# ============================================================
# DOCX READER
# ============================================================

def read_docx(path: Path) -> str:
    """
    Extract text from DOCX.
    """

    document = Document(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    extracted_text = "\n".join(paragraphs).strip()

    if not extracted_text:
        return "Error reading DOCX: No text could be extracted."

    return extracted_text


# ============================================================
# TXT READER
# ============================================================

def read_txt(path: Path) -> str:
    """
    Extract text from TXT.
    """

    text = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    text = text.strip()

    if not text:
        return "Error reading TXT: File is empty."

    return text


# ============================================================
# MAIN DOCUMENT READER
# ============================================================

def read_document(filename: str) -> str:
    """
    Main document reader.

    Supported:
        PDF
        DOCX
        TXT
    """

    path = Path(filename)

    # --------------------------------------------------------
    # Check file exists
    # --------------------------------------------------------

    if not path.exists():
        return f"Contract file not found: {filename}"

    extension = path.suffix.lower()

    try:

        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        if extension == ".txt":
            return read_txt(path)

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        if extension == ".pdf":
            return read_pdf(path)

        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        if extension == ".docx":
            return read_docx(path)

        # ----------------------------------------------------
        # Unsupported
        # ----------------------------------------------------

        return (
            f"Unsupported file type: {extension}. "
            "Supported formats are PDF, DOCX and TXT."
        )

    except Exception as e:
        return f"Error reading document: {str(e)}"
