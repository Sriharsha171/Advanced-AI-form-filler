# main.py

from pdf_parser import extract_form_fields_from_pdf
from knowledge_base_parser import parse_knowledge_base
from bert_mapping import map_fields_to_knowledge_base
from image_processing import pdf_to_images, preprocess_image, detect_cells, is_cell_empty, get_field_name
from text_box import put_text_in_box, create_text_box_below
from text_formatting import format_text_as_in_pdf

import os

# Example usage
if __name__ == "__main__":
    pdf_path = "Dummy_Questionnaire.pdf"
    output_dir = "output_images"
    knowledge_base_path = "dummy_data.txt"
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if not os.path.exists(knowledge_base_path):
        raise FileNotFoundError(f"Knowledge base file not found: {knowledge_base_path}")

    form_fields = extract_form_fields_from_pdf(pdf_path)
    knowledge_base = parse_knowledge_base(knowledge_base_path)
    field_mappings = map_fields_to_knowledge_base(form_fields, knowledge_base)

    os.makedirs(output_dir, exist_ok=True)
    image_paths = pdf_to_images(pdf_path, output_dir)
    
    for page_num, image_path in enumerate(image_paths):
        img = cv2.imread(image_path)
        preprocessed = preprocess_image(img)
        cells = detect_cells(preprocessed)
        
        for field_name, fill_text in field_mappings.items():
            field_filled = False
            for cell in cells:
                x, y, w, h = cell
                if is_cell_empty(img, x, y, w, h):
                    current_field_name = get_field_name(img, x, y, w, h)
                    print(f"Detected field: {current_field_name}, Expected field: {field_name}")  # Debugging info
                    if current_field_name == field_name:
                        formatted_text, font_size = format_text_as_in_pdf(fill_text, w, h)
                        img = put_text_in_box(img, formatted_text, x, y, w, h)
                        field_filled = True
                        break
            
            if not field_filled:
                for cell in cells:
                    x, y, w, h = cell
                    current_field_name = get_field_name(img, x, y, w, h)
                    if current_field_name == field_name:
                        img = create_text_box_below(img, x, y, w, h, fill_text)
                        break
        
        output_image_path = os.path.join(output_dir, f"filled_page_{page_num + 1}.png")
        cv2.imwrite(output_image_path, img)
        print(f"Filled page saved: {output_image_path}")

    print("Process completed!")
