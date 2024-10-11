

---

# Web Scraper with PDF Text Extraction

This is a Python-based web scraping tool that scrapes all text and links from a website, downloads PDFs, and extracts text from them using OCR (Optical Character Recognition) when necessary. The scrapped content is saved in a folder named after the base domain, with each link’s content saved in separate text files.

## Features

- **Recursive Scraping**: Scrapes all text and links from the base URL, following internal links only.
- **PDF Handling**: Downloads PDF files, extracts text using both `PyPDF2` and OCR with `pytesseract` for better text accuracy.
- **Organized Output**: Saves all scrapped content in a folder named after the base URL domain.
- **Failsafe PDF Text Extraction**: Uses OCR fallback when normal PDF text extraction fails.
- **File Naming**: Automatically names the text files based on the content (e.g., page text or PDF files).

## Requirements

Ensure you have the following dependencies installed:

```bash
pip install requests beautifulsoup4 PyPDF2 pytesseract pdf2image
sudo apt install tesseract-ocr poppler-utils  # For OCR and PDF image conversion
```

### Required Python Libraries

- **Requests**: To make HTTP requests.
- **BeautifulSoup4**: For parsing HTML content.
- **PyPDF2**: For extracting text from PDFs.
- **Pytesseract**: For OCR (Optical Character Recognition) when PDFs contain images instead of text.
- **pdf2image**: To convert PDF pages into images for OCR processing.

## How to Run

1. Clone or download this repository.
2. Open a terminal and navigate to the folder containing `web.py`.
3. Run the Python script:

    ```bash
    python scrapbot.py
    ```

4. When prompted, enter the base URL of the website you wish to scrape. For example:

    ```bash
    Enter the base URL to scrape: https://example.com
    ```

5. The scraper will create a folder named after the base URL’s domain (e.g., `example_com`), where it will store all scrapped content.

## How It Works

- The script starts by scraping the main page of the given URL.
- It saves the text content of each HTML page in a text file named `page_content.txt`.
- It follows all internal links, recursively scraping and saving the content of each page.
- If a PDF file is found, it is downloaded, and the text is extracted from it (using OCR for image-based PDFs).
- The extracted PDF text is saved in a text file with the suffix `_extracted.txt`.

## Example Output Structure

For a base URL of `https://example.com`, the output structure would look like this:

```
example_com/
    page_content.txt
    document1.pdf
    document1_extracted.txt
    another_page_content.txt
    ...
```

## Notes

- **Staying on the base URL**: The scraper only follows links that are internal (belonging to the same base domain).
- **PDF Extraction**: If the text extracted from the PDF is insufficient, the script falls back to using OCR for better accuracy.
- **File Naming**: Text files from pages and PDFs are named after the respective page or document they were scraped from.

## Troubleshooting

- **SSL Errors**: If you encounter SSL certificate errors (e.g., certificate verification issues), try disabling SSL verification for requests by modifying the request code to:

    ```python
    response = requests.get(base_url, verify=False)
    ```

- **OCR Text Issues**: Ensure that `pytesseract` and `poppler-utils` are correctly installed for proper OCR functionality on PDFs with images.

## License

This project is licensed under the MIT License.

---

**Disclaimer**: This is a basic scraper and may not work perfectly for all websites. 