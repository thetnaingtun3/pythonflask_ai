import os
import pytest
from app import create_app


@pytest.fixture
def client():
    # Create a test client for the Flask app
    app = create_app()
    app.config["TESTING"] = True
    app.config["UPLOAD_FOLDER"] = "data"
    with app.test_client() as client:
        yield client


def test_answer_question_success(client):
    # Test the /question endpoint with valid input
    response = client.post(
        "/question",
        json={"question": "What is the content of the articles?"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "answer" in data


def test_answer_question_no_question(client):
    # Test the /question endpoint with missing question
    response = client.post("/question", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "Question not provided"


def test_upload_file_success(client):
    # Test the /upload endpoint with a valid .txt file
    file_path = os.path.join(os.path.dirname(__file__), "test_file.txt")
    with open(file_path, "w") as f:
        f.write("This is a test file.")

    with open(file_path, "rb") as test_file:
        response = client.post(
            "/upload",
            data={"file": (test_file, "test_file.txt")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "uploaded successfully" in data["message"]

    # Clean up the uploaded file
    uploaded_file_path = os.path.join("data", "test_file.txt")
    if os.path.exists(uploaded_file_path):
        os.remove(uploaded_file_path)

    # Clean up the test file
    if os.path.exists(file_path):
        os.remove(file_path)


def test_upload_file_no_file(client):
    # Test the /upload endpoint with no file
    response = client.post("/upload", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "No file part in the request"


def test_upload_file_invalid_extension(client):
    # Test the /upload endpoint with an invalid file extension
    file_path = os.path.join(os.path.dirname(__file__), "test_file.pdf")
    with open(file_path, "w") as f:
        f.write("This is a test file.")

    with open(file_path, "rb") as test_file:
        response = client.post(
            "/upload",
            data={"file": (test_file, "test_file.pdf")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "Only .txt files are allowed"

    # Clean up the test file
    if os.path.exists(file_path):
        os.remove(file_path)
