## functions for pre-processing pdf-files
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
import pdfplumber

#extract text from pdf
def extract_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    #remove puncuation and newline characters
    pattern1 = r"[^\w\s']"
    pattern2 = '\n'
    text = re.sub(pattern1, '', text)
    text = re.sub(pattern2, ' ', text)

    #tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Convert tokens back to text
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text

def process_pdfs(folder_path, output_folder):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        
        # Extract text using pre-defined function
        extracted_text = extract_text(pdf_path)
        
        # Preprocess extracted text using pre-defined function
        preprocessed_text = preprocess_text(extracted_text)
        
        # Save preprocessed text to a new text file
        output_file_path = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.txt')
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(preprocessed_text)
        
        print('Preprocessing for doc done')