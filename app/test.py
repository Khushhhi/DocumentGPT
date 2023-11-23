from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS #for handling cross-origin requests
from PyPDF2 import PdfReader #for reading texts from pdfs
import io 

app = Flask(__name__)
CORS(app) #allows browser to permit requests from specified origins.


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template("upload.html")

    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'No file provided'}), 400

    try:
        if file.filename.endswith('.pdf'):
            reader = PdfReader(file)

            if reader.is_encrypted:
                return jsonify({'error': 'Encrypted PDFs are not supported'}), 400

            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()

            if not text.strip():
                return jsonify({'error': 'No text found in the PDF'}), 400

        elif file.filename.endswith('.txt'):
            try:
                text = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return jsonify({'error': 'Unable to decode text file. Ensure it is UTF-8 encoded.'}), 400

        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True)