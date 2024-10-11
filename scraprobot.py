import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# Function to save text content to a file
def save_text_to_file(folder, filename, content):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved content to {filepath}")

# Function to extract text from PDFs, with OCR fallback
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        # Attempt to extract text using PyPDF2
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

        # If extracted text is mostly empty or gibberish, fall back to OCR
        if not text.strip() or len(text) < 100:
            print(f"Using OCR for {pdf_path} due to insufficient readable text.")
            text = extract_text_from_pdf_with_ocr(pdf_path)

        return text
    except Exception as e:
        print(f"An error occurred while extracting text from {pdf_path}: {e}")
        return ""

# OCR extraction for PDFs (for scanned images or complex PDFs)
def extract_text_from_pdf_with_ocr(pdf_path):
    try:
        text = ""
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        # Apply OCR on each image
        for i, image in enumerate(images):
            ocr_text = pytesseract.image_to_string(image)
            text += f"\n\n--- Page {i + 1} ---\n\n{ocr_text}"
        
        return text
    except Exception as e:
        print(f"An error occurred while performing OCR on {pdf_path}: {e}")
        return ""

# Function to download PDF files and extract text
def download_and_extract_pdf(base_url, pdf_url, output_folder):
    pdf_filename = os.path.basename(pdf_url)
    pdf_filepath = os.path.join(output_folder, pdf_filename)
    
    try:
        # Download the PDF
        pdf_response = requests.get(pdf_url)
        with open(pdf_filepath, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"Downloaded PDF: {pdf_url}")

        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(pdf_filepath)
        if pdf_text:
            # Save extracted text to a file
            text_filename = pdf_filename.replace('.pdf', '_extracted.txt')
            save_text_to_file(output_folder, text_filename, pdf_text)
    except Exception as e:
        print(f"An error occurred while downloading or processing PDF {pdf_url}: {e}")

# Function to scrape the URL and process the content
def scrape_url(base_url, output_folder, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    # Ensure the URL hasn't been visited yet
    if base_url in visited_urls:
        return
    visited_urls.add(base_url)

    print(f"Scraping: {base_url}")

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text from the current page
        page_text = soup.get_text(separator='\n', strip=True)
        save_text_to_file(output_folder, 'page_content.txt', page_text)

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_base_url = urlparse(base_url).netloc
            parsed_full_url = urlparse(full_url).netloc

            # Stay within the base domain
            if parsed_full_url != parsed_base_url:
                continue

            # Handle PDFs
            if full_url.endswith('.pdf'):
                download_and_extract_pdf(base_url, full_url, output_folder)
            else:
                # Recursively scrape other URLs
                scrape_url(full_url, output_folder, visited_urls)
    except Exception as e:
        print(f"An error occurred while scraping {base_url}: {e}")

# Main function
def main():
    # Base URL to scrape
    base_url = input("Enter the base URL to scrape: ")
    
    # Create folder named after base URL's domain
    parsed_base_url = urlparse(base_url).netloc.replace('.', '_')
    output_folder = os.path.join(os.getcwd(), parsed_base_url)

    # Create directory for the scraped content
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print(f"Initiating scraper for: {base_url}")
    scrape_url(base_url, output_folder)

if __name__ == "__main__":
    main()
