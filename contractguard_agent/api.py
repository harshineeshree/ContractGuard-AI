from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .pipeline import analyze_contract_file


app = FastAPI(
    title="ContractGuard AI",
    description="AI-powered contract intelligence and compliance API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent

CONTRACTS_FOLDER = BASE_DIR / "contracts"
CONTRACTS_FOLDER.mkdir(parents=True, exist_ok=True)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ContractGuard AI",
    }


@app.post("/api/contracts/analyze")
async def analyze_contract(file: UploadFile = File(...)):

    if not file.filename:
        return {
            "error": "No file selected"
        }

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt",
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        return {
            "error": "Unsupported file type. Please upload PDF, DOCX or TXT."
        }

    safe_filename = Path(file.filename).name

    file_path = CONTRACTS_FOLDER / safe_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # IMPORTANT:
    # Analyze the actual uploaded/saved file.
    report = analyze_contract_file(str(file_path))

    return {
        "filename": safe_filename,
        "report": report,
    }


@app.get("/api/contracts")
def get_contracts():

    from .database import supabase

    response = (
        supabase
        .table("contracts")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "contracts": response.data
    }