from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

#create a folder to store the uploaded files

UPLOAD_FOLDER = "/Users/saksham/Desktop/fastapi/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#this mounts the folder to the server in which the files will be uploaded
app.mount("/files", StaticFiles(directory=UPLOAD_FOLDER), name="files")

#api endpoint to upload the file
#we used UploadFile from fastapi to handle the file upload its type of a class to hanfle with the file
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if not filename:
              raise HTTPException(status_code=400, detail="No file uploaded")

        with open(file_path, "wb") as f:
              shutil.copyfileobj(file.file, f) #copy the file to the folder
              return {
                    "filename": filename,
                    "file_path": file_path,
                    "status": "Uploaded successfully"
                      }


@app.get("/download/{filename}")
def downloader(filename: str):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not file_path:
              raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(file_path)


