# text_formatting.py

from PIL import ImageFont, ImageDraw, Image

def format_text_as_in_pdf(text, field_width, field_height, max_font_size=38, min_font_size=10):
    dummy_img = Image.new('RGB', (field_width, field_height))
    draw = ImageDraw.Draw(dummy_img)
    
    font_size = max_font_size
    while font_size >= min_font_size:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if text_width <= field_width and text_height <= field_height:
            break
        
        font_size -= 1
    
    return text, font_size
