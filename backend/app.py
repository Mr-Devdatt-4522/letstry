from flask import Flask, request, send_file
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import zipfile, os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow React frontend to call Flask backend

@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files["pdf"]
    if pdf_file.filename == "":
        return "No selected file", 400
    
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # zoom for quality
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_bytes = BytesIO()
            img.save(img_bytes, format="JPEG", quality=90)
            img_bytes.seek(0)
            zipf.writestr(f"page_{page_num+1}.jpg", img_bytes.read())
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
