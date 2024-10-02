# text_box.py

from PIL import Image, ImageDraw, ImageFont
import cv2

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
        if bbox[2] - bbox[0] <= w - 2*margin:
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

def create_text_box_below(img, x, y, w, h, text, color=(0, 0, 0)):
    new_y = y + h + 10
    new_h = h
    new_x = x
    new_w = w
    img = put_text_in_box(img, text, new_x, new_y, new_w, new_h, color=color)
    return img
