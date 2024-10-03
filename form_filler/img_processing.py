import cv2
import numpy as np
import pytesseract
from pdf2img import pdf_to_images
from text_processing import format_text_as_in_pdf
from PIL import Image, ImageDraw, ImageFont


pdf_path = "Dummy_Questionnaire.pdf"
output_dir = "output_images"

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    return denoised

def detect_cells(gray):
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cells = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 3000 < area < 200000:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20:
                cells.append((x, y, w, h))
    return cells

def is_cell_empty(img, x, y, w, h):
    cell = img[y:y + h, x:x + w]
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    white_pixel_ratio = np.sum(binary == 255) / (w * h)
    return white_pixel_ratio > 0.95

def get_field_name(img, x, y, w, h):
    left_cell = img[y:y + h, 0:x]
    left_text = pytesseract.image_to_string(left_cell)
    return left_text.strip() if left_text.strip() else "Unknown Field"

def put_text_in_box(img, text, x, y, w, h, color=(0, 0, 0), align_left=False, align_top=False):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    formatted_text, font_size = format_text_as_in_pdf(text, w, h)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    margin = 5
    line_spacing = 8
    lines = []
    words = formatted_text.split()
    current_line = words[0]
    for word in words[1:]:
        bbox = draw.textbbox((0, 0), current_line + " " + word, font=font)
        if bbox[2] - bbox[0] <= w - 2 * margin:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    bbox = draw.textbbox((0, 0), "A", font=font)
    line_height = bbox[3] - bbox[1] + line_spacing
    total_text_height = len(lines) * line_height - line_spacing

    for i, line in enumerate(lines):
        if align_top:
            text_y = y + margin + i * line_height
        else:
            text_y = y + (h - total_text_height) // 2 + i * line_height

        bbox = draw.textbbox((0, 0), line, font=font)
        if align_left:
            text_x = x + margin
        else:
            text_x = x + (w - (bbox[2] - bbox[0])) // 2

        for offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            draw.text((text_x + offset[0], text_y + offset[1]), line, font=font, fill=color)

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
