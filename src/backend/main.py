from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import shutil
import uuid

HERE = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(HERE, "..", "frontend"))
UPLOADS = os.path.join(HERE, "uploads")
os.makedirs(UPLOADS, exist_ok=True)

app = FastAPI()

# simple in-memory items list (replace with DB in production)
items: list = []


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())[:8]
    filename = f"{uid}_{file.filename}"
    dest = os.path.join(UPLOADS, filename)
    with open(dest, "wb") as out:
        shutil.copyfileobj(file.file, out)
    item = {"id": uid, "name": file.filename, "status": "uploaded", "path": dest}
    items.append(item)
    return JSONResponse({"ok": True, "item": item})


@app.get("/items")
def list_items():
    return {"items": items}


# serve frontend static files
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
