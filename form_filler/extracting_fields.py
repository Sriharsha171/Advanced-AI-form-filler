import fitz

def extract_form_fields_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    form_fields = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            if len(block) >= 5:
                x0, y0, x1, y1 = block[:4]
                field_text = block[4].strip()
                if field_text:
                    form_fields.append({
                        "page": page_num + 1,
                        "coordinates": (x0, y0, x1, y1),
                        "field_name": field_text
                    })
    return form_fields