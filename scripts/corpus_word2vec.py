# Script for Creating Different Corpora and Traiing Word2Vec Models on Risk Analysis Reports

####### Imports #######
import os
import pandas as pd
from webutils.preprocessing_utils import extract_text, process_pdfs, create_corpus
from webutils.analysis_utils import calculate_tfidf
from gensim.models import Word2Vec
import pickle

################################# ANALYSIS ON FULL CORPUS #################################

####### Pre-Processing Data #######

#define folder paths
raw_data = '../data/raw_data'
preprocessed_data = '../data/preprocessed_data'
corpus_folder = '../data/corpus'


# extract text from pdf, pre-process and save as txt file
#preprocessing includes removing stopwords and punctuation, lowercasing and lemmetizing
os.makedirs(preprocessed_data, exist_ok=True)
os.makedirs(corpus_folder, exist_ok=True)
process_pdfs(raw_data, preprocessed_data)
print('Preprocessing done.')
#turn txt files into tokenized corpus
corpus = create_corpus(preprocessed_data)
print(f'Full Corpus created. {len(corpus)} documents in corpus.')

# Save corpus
corpus_file_path = os.path.join(corpus_folder, 'corpus.pkl')
with open(corpus_file_path, 'wb') as f:
    pickle.dump(corpus, f)
print('Full Corpus saved.')

####### TF-IDF #######

# Calculate TF-IDF matrix, feature names, and file names and store in df
tfidf_scores = calculate_tfidf(corpus, folder_path=preprocessed_data)
os.makedirs('../results', exist_ok=True)
tfidf_df = pd.DataFrame(tfidf_scores).to_csv('../results/tfidf.csv')
print('TF-IDF (Full Corpus) done.')

####### Most Similar Words with Word2Vec #######

#train word2vec model
model = Word2Vec(sentences=corpus, vector_size=150, window=3, min_count=1, sg=1, epochs=10)
print('Word2Vec model trained.')

#save model
os.makedirs('../model', exist_ok=True)
model.save('../model/word2vec_model_full.model')
print('Full Word2Vec Model saved.')

################################# ANALYSIS ON ANNUAL REPORTS ONLY #################################

####### Pre-Processing Data #######

#move copy of preprocessed files that contain risk_analysis in filename tonew folder
preprocessed_data_annual = '../data/preprocessed_data_annual'
os.makedirs(preprocessed_data_annual, exist_ok=True)

#move copy of annual risk analysis files to newly created folder
annual_reports = [f for f in sorted(os.listdir(preprocessed_data)) if 'analysis' in f]
for report in annual_reports:
    report_path = os.path.join(preprocessed_data, report)
    new_report_path = os.path.join(preprocessed_data_annual, report)
    with open(report_path, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(new_report_path, 'w', encoding='utf-8') as f:
        f.write(text)

#delete falsely selected file
os.remove(os.path.join(preprocessed_data_annual, 'common-integrated-risk-analysis-model-version-summary-booklet-2.1.txt'))

corpus_annual = create_corpus(preprocessed_data_annual)
print(f'Annual Corpus created. {len(corpus_annual)} documents in corpus.')

# Save corpus
corpus_file_path_annual = os.path.join(corpus_folder, 'corpus_annual.pkl')
with open(corpus_file_path_annual, 'wb') as f:
    pickle.dump(corpus_annual, f)
print('Annual Corpus saved.')

####### TF-IDF #######

# Calculate TF-IDF matrix, feature names, and file names and store in df
tfidf_scores_annual = calculate_tfidf(corpus_annual, folder_path=preprocessed_data_annual)
tfidf_df = pd.DataFrame(tfidf_scores_annual).to_csv('../results/tfidf_annual.csv')
print('TF-IDF (Annual) done.')


####### Word2Vec #######

#train another word2vec model, but only on annual corpus
model_annual = Word2Vec(sentences=corpus_annual, vector_size=50, window=3, min_count=1, sg=1, epochs=10)
#save model
model_annual.save('../model/word2vec_model_annual.model')
print('Annual Word2Vec Model saved.')

####### Unpreprocessed-Corpus for Word Cloud #######

#create corpus of un-pre-processed annual reports for wordcloud
annual_raw_reports = [extract_text(f) for f in sorted(os.listdir(raw_data)) 
                      if 'analysis' in f and 
                      f != 'common-integrated-risk-analysis-model-version-summary-booklet-2.1.pdf']
corpus_annual_raw= create_corpus(annual_raw_reports)
print(f'Unpreprocessed Corpus created. {len(corpus_annual_raw)} documents in corpus.')

#save corpus 
corpus_file_path_annual_raw = os.path.join(corpus_folder, 'corpus_annual_raw.pkl')
with open(corpus_file_path_annual_raw, 'wb') as f:
    pickle.dump(corpus_annual_raw, f)
print('Annual Un-Preprocessed Corpus saved.')