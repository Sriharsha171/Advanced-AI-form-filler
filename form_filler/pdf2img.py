import os
import fitz


def pdf_to_images(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # Increase resolution
        img_path = os.path.join(output_dir, f'template_{page_num + 1}.png')
        pix.save(img_path)
        images.append(img_path)
    doc.close()
    return images