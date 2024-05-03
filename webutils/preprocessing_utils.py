## functions for pre-processing pdf-files
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
    pattern3 = r'\d+'
    text = re.sub(pattern1, '', text)
    text = re.sub(pattern2, ' ', text)
    text = re.sub(pattern3, ' ', text)

    #tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    #lemmetize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Convert tokens back to text
    preprocessed_text = ' '.join(lemmatized_tokens)
    
    return preprocessed_text


#combine both pre-processing steps in one function and store file as txt in new folder
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

#load txt files and turn them into tokenized corpus
def create_corpus(folder_path):
    tokenized_corpus = []

    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.txt'):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                text = f.read()
                tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
                tokenized_corpus.append(tokens)
    
    return tokenized_corpus