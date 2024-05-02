# Script for performing NLP on Risk Analysis Reports

#imports
import os
from webutils.preprocessing_utils import process_pdfs

# extract text from pdf, pre-process and save as txt file
folder_path = '../data/raw_data'
output_folder = '../data/preprocessed_data'
os.makedirs('../data/preprocessed_data', exist_ok=True)

process_pdfs(folder_path, output_folder)
