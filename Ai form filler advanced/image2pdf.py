def image_to_pdf(image_path, output_pdf_path):
    image = Image.open(image_path)
    pdf_bytes = image.convert('RGB')
    pdf_bytes.save(output_pdf_path, "PDF", resolution=100.0)
    print(f"PDF saved: {output_pdf_path}")
