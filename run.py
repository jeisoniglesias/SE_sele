import os
from app import create_app

app = create_app()
UPLOAD_FOLDER = "uploads"

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.run(debug=True)
