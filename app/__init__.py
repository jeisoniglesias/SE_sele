import base64
import os
from dotenv import load_dotenv

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_file,
    flash,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

from app.common.asistente import Asisitente
from app.controller.antiguo import AntiguoController


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "uploads"
    )
    app.config["SECRET_KEY"] = "mi_clave_secreta"
    asistente = Asisitente()

    @app.route("/")
    def index():
        return render_template("index.html")

    antiguoController = AntiguoController(assistant=asistente)

    @app.route("/analisis", methods=["GET", "POST"])
    def analisis():
        if request.method == "POST":
            image = request.files.get("image")

            # Validar la imagen con una función modular
            if not image or image.filename == "":
                flash("No se ha seleccionado una imagen", "error")
                return redirect(url_for("analisis"))
            if not antiguoController.allowed_file(image.filename):
                flash("Formato de archivo no permitido", "error")
                return redirect(url_for("analisis"))

            # Guardar la imagen de manera segura
            filename = secure_filename(image.filename)
            filePath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filePath)

            # Procesar la imagen
            encode = antiguoController.encode_image(filePath)
            response = antiguoController.process(encode)

            return render_template("analisis.html", image_name=filename, data=response)

        return render_template("analisis.html")

    @app.route("/image/<string:image_name>")
    def show_image(image_name):
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
        return send_file(image_path)

    return app
