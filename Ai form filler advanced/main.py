import fitz  # PyMuPDF
import cv2
import pytesseract
import numpy as np
import re

def parse_knowledge_base(file_path):
    knowledge_base = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.match(r'(.+?):\s*(.+)', line)
            if match:
                key, value = match.groups()
                knowledge_base[key.strip()] = value.strip()
    return knowledge_base

# Convert PDF to images
def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        img = img.copy()
        images.append(img)

    return images

# Preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    return thresh

# Detect tables in the image
def detect_tables(thresh_image):
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tables = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (100 < w < 800) and (50 < h < 400):
            tables.append((x, y, w, h))

    return tables

# Extract text using Tesseract OCR
def extract_text_from_image(image, box):
    x, y, w, h = box
    roi = image[y:y + h, x:x + w]
    text = pytesseract.image_to_string(roi)
    return text.strip()

# Process each detected table
def process_table(image, table):
    x, y, w, h = table
    full_text = extract_text_from_image(image, table)

    rows = full_text.split('\n')

    # Remove empty rows
    rows = [row for row in rows if row.strip()]

    grouped_rows = []
    current_row = []

    for row in rows:
        if re.search(r'\b(What|How|When|Where|Who|Which|Is|Are|Was|Were|Do|Does|Did)\b', row) or len(current_row) == 0:
            if current_row:
                grouped_rows.append(' '.join(current_row))
            current_row = [row]
        else:
            current_row.append(row)

    if current_row:
        grouped_rows.append(' '.join(current_row))

    for row_index, row in enumerate(grouped_rows):
        columns = row.rsplit(' ', 1)

        if len(columns) == 2:
            question = columns[0].strip()
            answer = columns[1].strip()

            row_height = h // len(grouped_rows)

            question_box = (x, y + row_index * row_height, x + w // 2, y + (row_index + 1) * row_height)
            answer_box = (x + w // 2, y + row_index * row_height, x + w, y + (row_index + 1) * row_height)

            cv2.rectangle(image, (question_box[0], question_box[1]), (question_box[2], question_box[3]), (0, 0, 255),
                          1)  # Red for questions field
            cv2.rectangle(image, (answer_box[0], answer_box[1]), (answer_box[2], answer_box[3]), (0, 255, 0),
                          1)  # Green for answers field

            print(f"Detected Question: {question} - Detected Answer: {answer}")

def process_image(image):
    thresh = preprocess_image(image)
    tables = detect_tables(thresh)

    for table in tables:
        process_table(image, table)

    cv2.imshow('Detected Tables', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

pdf_path = 'Dummy_Questionnaire.pdf'
data_path = 'Dummy_data.txt'

# Parse and print the knowledge base
knowledge_base = parse_knowledge_base(data_path)
print("Knowledge Base:")
for key, value in knowledge_base.items():
    print(f"{key}: {value}")

images = convert_pdf_to_images(pdf_path)

for i, img in enumerate(images):
    print(f"Processing page {i + 1}")
    process_image(img)
