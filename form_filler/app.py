from flask import Flask, request, redirect, url_for, send_file, render_template_string
import os
import cv2
from extracting_fields import extract_form_fields_from_pdf
from filling import fill_form_fields
from img2pdf import image_to_pdf
from img_processing import preprocess_image, detect_cells, is_cell_empty, get_field_name, put_text_in_box
from kdb import parse_knowledge_base
from mapping import map_fields_to_knowledge_base
from pdf2img import pdf_to_images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'forms'
app.config['OUTPUT_FOLDER'] = 'outputs/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# HTML Template as a string with CSS styles
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI PDF Form Filler</title>
    <style>
        body {
            background-color: #0D0D0D;
            color: #E0E0E0;
            font-family: 'Roboto', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        h1, h2 {
            text-align: center;
            color: #00FFB3;
        }
        form {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 255, 179, 0.5);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        input[type="file"] {
            margin: 20px 0;
            color: #00FFB3;
            border: 1px solid #00FFB3;
            padding: 10px;
            background-color: transparent;
            border-radius: 5px;
            width: 250px;
        }
        button {
            background-color: #00FFB3;
            color: #0D0D0D;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #00CC8C;
        }
        a {
            color: #00FFB3;
            text-decoration: none;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            margin-top: 20px;
            display: inline-block;
            transition: background-color 0.3s ease;
        }
        a:hover {
            background-color: #00CC8C;
        }
    </style>
</head>
<body>
    <div>
        <h1>AI PDF Form Filler</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="pdf_file" required>
            <button type="submit">Fill the Form Using AI</button>
        </form>
        {% if filled_pdf %}
            <h2>Your filled PDF is ready!</h2>
            <a href="{{ url_for('download', filename=filled_pdf.split('/')[-1]) }}" download>Download Filled PDF</a>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return redirect(url_for('index'))
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return redirect(url_for('index'))

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    knowledge_base_path = "Dummy_data.txt"
    form_fields = extract_form_fields_from_pdf(pdf_path)
    knowledge_base = parse_knowledge_base(knowledge_base_path)
    field_mappings = map_fields_to_knowledge_base(form_fields, knowledge_base)

    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    image_paths = pdf_to_images(pdf_path, app.config['OUTPUT_FOLDER'])

    for page_num, image_path in enumerate(image_paths):
        img = cv2.imread(image_path)
        preprocessed = preprocess_image(img)
        cells = detect_cells(preprocessed)
        img = fill_form_fields(img, field_mappings, cells)
        output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], f"filled_page_{page_num + 1}.png")
        cv2.imwrite(output_image_path, img)
        output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f"filled_form_{page_num + 1}.pdf")
        image_to_pdf(output_image_path, output_pdf_path)

    filled_pdf_filename = f"filled_form_1.pdf"  

    return render_template_string(HTML_TEMPLATE, filled_pdf=filled_pdf_filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
