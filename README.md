# Advanced-AI-form-filler

This the advanced version of using AI to fill the forms

## Features

- Extracts form fields from PDF documents.
- Maps extracted fields to a knowledge base using BERT for better accuracy.
- Fills in the identified form fields with relevant data.
- Supports image preprocessing for improved text extraction.
- Outputs the filled PDF with data inserted in the correct fields.

## Technologies Used

- **Python**: Programming language.
- **PyMuPDF (fitz)**: For PDF processing.
- **OpenCV**: For image processing.
- **Pytesseract**: For optical character recognition (OCR).
- **Pillow (PIL)**: For image manipulation.
- **Transformers**: For natural language processing (BERT).
- **NumPy**: For numerical operations.
- **Scikit-learn**: For machine learning utilities.


project/
│
├── main.py                       # The main script to run the application
├── knowledge_base.py              # Script for knowledge base parsing
├── form_fields_extractor.py       # Script for extracting form fields from PDF
├── bert_encoder.py                # Script for BERT text encoding
├── form_mapping.py                # Script for mapping form fields to knowledge base
├── pdf_processing.py              # Script for PDF to image conversion and image preprocessing
├── ocr_utils.py                   # Script for OCR-related functions (detecting cells, reading text, etc.)
└── utils.py                       # Miscellaneous utilities (text formatting, putting text in boxes, etc.)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-PDF-Filler.git
   cd AI-PDF-Filler/src
   






