# Instalar pacote pdfkit
# pip install -q pdfkit

# Instalar o pacote wkhtmltopdf
# macos -> brew install --cask wkhtmltopdf

import os
import pdfkit
from bs4 import BeautifulSoup

def preprocess_html(input_html, output_html):
    """
    Preprocess HTML to ensure long text and images fit within A4 format.
    Args:
        input_html (str): Path to the input HTML file.
        output_html (str): Path to save the modified HTML file.
    """
    with open(input_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Add CSS to avoid word splitting and resize images
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
    @media print {
        .page-break {
            page-break-before: always;
        }
    }
    """
    soup.head.append(style_tag)

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
    }

    try:
        pdfkit.from_file(input_html, output_pdf, options=options, configuration=config)
        print(f"PDF successfully created: {output_pdf}")
    except Exception as e:
        print(f"Error during PDF creation: {e}")


# CONFIGURACAO DOS PARAMETROS
RELATIVE_HTML_FILES_DIR = os.path.join(os.getcwd(), "data/example2")
HTML_FILE_NAME = "PRJD16.html"
PREPROCESSED_TEMP_HTML = "preprocessed.html"
OUTPUT_PDF_FILE_NAME = "output.pdf"
WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'

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