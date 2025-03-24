import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    # Open the PDF file using PyMuPDF (fitz)
    doc = fitz.open(file_path)
    text = ""
    
    # Loop through each page and extract text
    for page in doc:
        text += page.get_text()
    
    # Close the document to free resources
    doc.close()
    
    # Return the full extracted text
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    # Split the full text into a list of words
    words = text.split()
    chunks = []

    # Generate overlapping chunks of words
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    # Return the list of text chunks
    return chunks

