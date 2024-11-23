from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path
import os
import io
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Directories for uploads and temporary storage
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Function to delete files after a delay
def delete_file_after_delay(file_path: Path, delay: int = 3600):
    import time
    time.sleep(delay)
    if file_path.exists():
        file_path.unlink()

# Function to add a password to the PDF
def add_pdf_password(pdf_buffer, password):
    """Encrypt a PDF file with a password."""
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(pdf_buffer)

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(password)

    output_buffer = BytesIO()
    pdf_writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer

# Function to convert .docx to PDF
def convert_docx_to_pdf(docx_file):
    """Convert a .docx file to a PDF and return the PDF as a buffer."""
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

    pdf_canvas.setFont("Helvetica", 12)

    doc = Document(docx_file)
    y_position = 720  
    margin = 50

    for para in doc.paragraphs:
        text = para.text

        if y_position < 50:
            pdf_canvas.showPage()
            y_position = 720

        try:
            pdf_canvas.drawString(margin, y_position, text)
        except Exception as e:
            pdf_canvas.drawString(margin, y_position, "[Unrenderable Text]")

        y_position -= 15

    pdf_canvas.save()
    pdf_buffer.seek(0)
    return pdf_buffer

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    password: str = None,
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are allowed.")

    # Save the uploaded file temporarily
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    metadata = {
        "name": file.filename,
        "size": file_path.stat().st_size / 1024,  # Size in KB
        "uploaded_at": datetime.now().isoformat(),
    }

    try:
        # Convert .docx to PDF
        pdf_buffer = convert_docx_to_pdf(file_path)

        # Add password protection if a password is provided
        if password:
            pdf_buffer = add_pdf_password(pdf_buffer, password)

        # Save the PDF to a temporary file for download
        pdf_filename = f"{file.filename.rsplit('.', 1)[0]}.pdf"
        pdf_path = UPLOAD_DIR / pdf_filename
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    # Schedule file deletion
    background_tasks.add_task(delete_file_after_delay, file_path)
    background_tasks.add_task(delete_file_after_delay, pdf_path)

    return {
        "metadata": metadata,
        "pdf_url": f"http://localhost:8000/files/{pdf_filename}",
    }

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
