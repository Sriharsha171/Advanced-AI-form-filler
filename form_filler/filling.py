from img_processing import is_cell_empty, get_field_name, put_text_in_box
from text_processing import format_text_as_in_pdf


def fill_form_fields(img, field_mappings, cells):
    for field_name, fill_text in field_mappings.items():
        for cell in cells:
            x, y, w, h = cell
            if is_cell_empty(img, x, y, w, h):
                current_field_name = get_field_name(img, x, y, w, h)
                if current_field_name == field_name:
                    formatted_text, font_size = format_text_as_in_pdf(fill_text, w, h)
                    img = put_text_in_box(img, formatted_text, x, y, w, h)
                    break
    return img