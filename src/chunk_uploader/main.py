from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi import requests, Request
import os

from upload_logic import save_chunk, check_upload_status, assemble_chunks

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/upload_chunk")
async def upload_chunk(
    file: UploadFile = File(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    file_id: str = Form(...),
    original_filename: str = Form(...)
):

    await save_chunk(file, chunk_index, file_id)

    status = check_upload_status(file_id, total_chunks)

    if status == "complete":
        final_path = await assemble_chunks(file_id, original_filename)
        return JSONResponse(content={"status": "assembled", "path": final_path})

    return JSONResponse(content={"status": "incomplete", "chunk_index": chunk_index})


@app.get("/upload-status/{file_id}/{total_chunks}")
async def status(file_id: str, total_chunks: int):
    status = check_upload_status(file_id, total_chunks)
    return {"status": status}
