import base64
from flask import session
from PIL import Image
import pytesseract
import os

class AntiguoController:
    def __init__(self, assistant):
        self.assistant = assistant

    def allowed_file(self, filename):
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
        )

    def construirPromt(self, text):
        return {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Return JSON document with data. Only return JSON not other text in spanish, In the event that the previous properties result in null or do not apply, I return a json with the noEsDocumento property in which a description of the image must be given. ",
                },
                {
                    "type": "image_url",
                    # for online images
                    # "image_url": {"url": image_url}
                    "image_url": {"url": f"data:image/png;base64,{text}"},
                },
            ],
        }

    def encode_image(self, image_file):
        # Check file size (20 MB = 20 * 1024 * 1024 bytes)
        if os.path.getsize(image_file.name) > 20 * 1024 * 1024:
            raise ValueError("Image file exceeds 20 MB size limit.")

        # Check supported formats
        allowed_extensions = ["png", "jpeg", "jpg", "gif", "webp"]
        file_extension = image_file.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            raise ValueError(
                f"Unsupported image format. Allowed formats are: {', '.join(allowed_extensions)}"
            )

        # Encode the image
        return base64.b64encode(image_file.read()).decode("utf-8")

    def getHistory(data):
        if "analisis_imagenes" in session:
            # Retorna la variable de sesión existente
            return session["analisis_imagenes"]
        else:
            # Crea la variable de sesión con el objeto dado y la asigna
            session["analisis_imagenes"] = [
                {
                    "role": "system",
                    "content": "You are an expert assistant in ancient documents, your role will be to identify what type of document it is, its name, its typography, what it is about, what it is about and if it is possible to transcribe it, all this in Spanish and answer the following questions",
                }
            ]
            # Retorna la variable de sesión recién creada
            return session["analisis_imagenes"]

    def process(self, encodeFile):
        history = self.getHistory()
        promt = self.construirPromt(encodeFile)
        history.append(promt)

        response = self.assistant.chat(history)
        response = response.replace("```json\n", "").replace("\n```", "")
        return response
