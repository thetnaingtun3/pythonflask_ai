from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
import os
from app.services import process_question, save_uploaded_file
from app.utils import simple_response, build_prompt, stream_openai

app = FastAPI()
data_folder = "data"  # Ensure this matches your folder structure

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins. Replace "*" with specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def home():
    return simple_response("home")


@app.post("/question")
async def answer_question(data: dict):
    if "question" not in data:
        raise HTTPException(status_code=400, detail="Question not provided")
    return process_question(data)


@app.post("/question/stream")
async def stream_answer_question(data: dict):
    if "question" not in data:
        raise HTTPException(status_code=400, detail="Question not provided")
    from app.utils import load_articles

    articles = load_articles(data_folder)
    combined_articles = "\n\n".join(articles.values())
    prompt = build_prompt(combined_articles, data["question"])

    def json_stream():
        yield '{"status": "success", "message": "Answer generated successfully", "answer": "'
        for chunk in stream_openai(prompt):
            yield chunk.replace('"', '\\"')  # Escape quotes for valid JSON
        yield '"}'

    return StreamingResponse(json_stream(), media_type="application/json")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the data folder."""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    try:
        file_path = os.path.join(data_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files")
async def list_files():
    """List all files in the data folder."""
    try:
        files = os.listdir(data_folder)
        return {"status": "success", "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{filename}")
async def read_file(filename: str):
    """Read the content of a specific file."""
    file_path = os.path.join(data_folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/files/{filename}")
async def update_file(filename: str, data: dict):
    """Update the content of a specific file."""
    file_path = os.path.join(data_folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    new_content = data.get("content", "")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        return {
            "status": "success",
            "message": f"File '{filename}' updated successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hello")
async def hello():
    return "Hello, haha!"
