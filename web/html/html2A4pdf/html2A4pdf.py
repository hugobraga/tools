# Instalar pacote pdfkit
# pip install -q pdfkit

# Instalar o pacote wkhtmltopdf
# macos -> brew install --cask wkhtmltopdf

import os
import pdfkit
from bs4 import BeautifulSoup

def preprocess_html(input_html, output_html):
    """
    Preprocess HTML to ensure long SQL code blocks and images fit within A4 format.
    Args:
        input_html (str): Path to the input HTML file.
        output_html (str): Path to save the modified HTML file.
    """
    with open(input_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Add CSS to prevent SQL from being cut, force proper wrapping, and ensure visibility
    style_tag = soup.new_tag("style")
    style_tag.string = """
    body, p {
        word-wrap: break-word;
        overflow-wrap: break-word;
        hyphens: none;
    }
    img {
        max-width: 190mm;
        height: auto;
    }
    pre, code {
        white-space: pre-wrap !important;  /* Ensures text wraps properly */
        word-break: break-word !important;
        text-overflow: clip !important;
        font-size: 9px !important;  /* Ensures more text fits on a single line */
        background-color: #f8f8f8;
        padding: 5px;
        border: 1px solid #ccc;
        display: table !important;  /* Allows content to expand */
        width: auto !important;  /* Removes width constraints */
        min-width: 100% !important; /* Forces block expansion */
        box-sizing: border-box !important;
        page-break-inside: avoid !important; /* Prevents SQL code from being split */
        overflow: hidden !important; /* Ensures full visibility */
    }
    .code-container {
        width: 100%;
        display: block;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto; /* Prevent table stretching */
    }
    td, th {
        border: 1px solid black;
        padding: 5px;
        font-size: 10px;
        word-break: break-word !important; /* Ensure table content wraps */
    }
    @media print {
        .page-break {
            page-break-before: always;
        }
    }
    """
    soup.head.append(style_tag)

    # Apply direct inline styles to <pre> and <code> elements
    for pre_tag in soup.find_all("pre"):
        pre_tag["style"] = "white-space: pre-wrap !important; word-break: break-word !important; display: table !important; width: auto !important; min-width: 100% !important; box-sizing: border-box !important; page-break-inside: avoid !important; padding: 5px !important; border: 1px solid #ccc;"

    for code_tag in soup.find_all("code"):
        code_tag["style"] = "white-space: pre-wrap !important; word-break: break-word !important; display: table !important; width: auto !important; min-width: 100% !important; box-sizing: border-box !important; page-break-inside: avoid !important; padding: 5px !important; border: 1px solid #ccc;"

    # Save the modified HTML
    with open(output_html, "w", encoding="utf-8") as file:
        file.write(str(soup))


def html_to_pdf(input_html, output_pdf, wkhtmltopdf_path):
    """
    Converts an HTML file to a PDF with A4 page size.
    Args:
        input_html (str): Path to the input HTML file.
        output_pdf (str): Path to the output PDF file.
        wkhtmltopdf_path (str): Path to the wkhtmltopdf executable.
    """
    # Configure path to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # PDF options
    options = {
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-right': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '15mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',  # Required to access local resources like images
        'print-media-type': '',
        'no-outline': None
    }

    try:
        pdfkit.from_file(input_html, output_pdf, options=options, configuration=config)
        print(f"PDF successfully created: {output_pdf}")
    except Exception as e:
        print(f"Error during PDF creation: {e}")


# CONFIGURACAO DOS PARAMETROS
RELATIVE_HTML_FILES_DIR = os.path.join(os.getcwd(), "data")
HTML_FILE_NAME = "PDPDSDJ2-2.html"
PREPROCESSED_TEMP_HTML = "preprocessed.html"
OUTPUT_PDF_FILE_NAME = "PORTDVDSIT-246.pdf"
WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf'

input_html_file = os.path.join(RELATIVE_HTML_FILES_DIR, HTML_FILE_NAME)
preprocessed_html_file = os.path.join(RELATIVE_HTML_FILES_DIR, PREPROCESSED_TEMP_HTML)
output_pdf_file = os.path.join(RELATIVE_HTML_FILES_DIR, OUTPUT_PDF_FILE_NAME)

# Preprocessa HTML e gera PDF
try:
    preprocess_html(input_html_file, preprocessed_html_file)
    html_to_pdf(preprocessed_html_file, output_pdf_file, WKHTMLTOPDF_PATH)
finally:
    # Delete the temporary file after PDF generation
    if os.path.exists(preprocessed_html_file):
        os.remove(preprocessed_html_file)