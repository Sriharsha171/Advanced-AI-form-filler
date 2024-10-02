# image_processing.py

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw, ImageFont

def pdf_to_images(pdf_path, output_dir):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
        img_path = os.path.join(output_dir, f'temp_page_{page_num + 1}.png')
        pix.save(img_path)
        images.append(img_path)
    doc.close()
    return images

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    return denoised

def detect_cells(gray):
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CCHAIN_APPROX_SIMPLE)
    cells = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 3000 < area < 200000:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20:
                cells.append((x, y, w, h))
    return cells

def is_cell_empty(img, x, y, w, h):
    cell = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    white_pixel_ratio = np.sum(binary == 255) / (w * h)
    return white_pixel_ratio > 0.95

def get_field_name(img, x, y, w, h):
    left_cell = img[y:y+h, 0:x]
    left_text = pytesseract.image_to_string(left_cell, config='--psm 6')
    return left_text.strip().lower() if left_text.strip() else "unknown field"
