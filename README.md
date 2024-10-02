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


AI-firm-filler-advanced/


├── main.py                       
├── knowledge_base.py             
├── form_fields_extractor.py       
├── bert_encoder.py               
├── form_mapping.py                
├── pdf_processing.py           
├── ocr_utils.py                   
└── utils.py                       

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-PDF-Filler.git
   cd AI-PDF-Filler/src
   






