from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from models import IngestRecord, ProcessRequest
from db import create_tables, insert_record, insert_ai_result
from ai import run_ai_enrichment

app = FastAPI(title="Sharkflow MVP")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    # process file rows with AI...
    ...
