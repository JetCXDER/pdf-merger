from flask import Flask, render_template, request, send_file, jsonify, url_for
import os
from PyPDF2 import PdfMerger

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    merger = PdfMerger()

    file_paths = []
    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        file_paths.append(path)
        merger.append(path)

    output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    merger.write(output_path)
    merger.close()

    # cleanup uploaded files
    for path in file_paths:
        os.remove(path)

    # Instead of auto download, return JSON with download URL
    return jsonify({"download_url": url_for("download_file")})

@app.route("/download")
def download_file():
    output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
