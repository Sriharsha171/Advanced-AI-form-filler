import os

import cv2

from extracting_fields import extract_form_fields_from_pdf
from filling import fill_form_fields
from img2pdf import image_to_pdf
from img_processing import preprocess_image, detect_cells
from kdb import parse_knowledge_base
from mapping import map_fields_to_knowledge_base
from pdf2img import pdf_to_images

if __name__ == "__main__":
    pdf_path = r"C:\Users\bksh1\Desktop\Advanced-AI-form-filler-main\ai\forms\Dummy_Questionnaire.pdf"
    output_dir = "outputs"
    knowledge_base_path = r"C:\Users\bksh1\Desktop\Advanced-AI-form-filler-main\ai\data\Dummy_data.txt"
    form_fields = extract_form_fields_from_pdf(pdf_path)

    # Parse the knowledge base
    knowledge_base = parse_knowledge_base(knowledge_base_path)

    # Map form fields to knowledge base entries using Sentence Transformers
    field_mappings = map_fields_to_knowledge_base(form_fields, knowledge_base)

    # Convert PDF to images
    os.makedirs(output_dir, exist_ok=True)
    image_paths = pdf_to_images(pdf_path, output_dir)

    for page_num, image_path in enumerate(image_paths):
        img = cv2.imread(image_path)
        preprocessed = preprocess_image(img)
        cells = detect_cells(preprocessed)

        # Fill the form fields in the image using the new function
        img = fill_form_fields(img, field_mappings, cells)

        # Save the filled image for the current page
        output_image_path = os.path.join(output_dir, f"filled_page_{page_num + 1}.png")
        cv2.imwrite(output_image_path, img)
        print(f"Filled page saved: {output_image_path}")

        # Convert the filled image to PDF
        output_pdf_path = os.path.join(output_dir, f"filled_page_{page_num + 1}.pdf")
        image_to_pdf(output_image_path, output_pdf_path)