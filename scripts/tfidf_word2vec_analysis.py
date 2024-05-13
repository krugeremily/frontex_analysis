# Script for performing NLP on Risk Analysis Reports

####### Imports #######
import os
import pandas as pd
from webutils.preprocessing_utils import process_pdfs, create_corpus
from webutils.analysis_utils import calculate_tfidf
from gensim.models import Word2Vec
import pickle


####### Pre-Processing Data #######

# extract text from pdf, pre-process and save as txt file
#preprocessing includes removing stopwords and punctuation, lowercasing and lemmetizing
raw_data = '../data/raw_data'
preprocessed_data = '../data/preprocessed_data'
corpus_folder = '../data/corpus'
os.makedirs(preprocessed_data, exist_ok=True)
os.makedirs(corpus_folder, exist_ok=True)
process_pdfs(raw_data, preprocessed_data)
print('Preprocessing done.')
#turn txt files into tokenized corpus
corpus = create_corpus(preprocessed_data)
print(f'Corpus created. {len(corpus)} documents in corpus.')

# Save corpus
corpus_file_path = os.path.join(corpus_folder, 'corpus.pkl')
with open(corpus_file_path, 'wb') as f:
    pickle.dump(corpus, f)
print('Corpus saved.')

####### TF-IDF #######

# Calculate TF-IDF matrix, feature names, and file names and store in df
tfidf_scores = calculate_tfidf(corpus, folder_path=preprocessed_data)
os.makedirs('../results', exist_ok=True)
tfidf_df = pd.DataFrame(tfidf_scores).to_csv('../results/tfidf.csv')
print('TF-IDF done.')

####### Most Similar Words with Word2Vec #######

#train word2vec model
model = Word2Vec(sentences=corpus, vector_size=150, window=3, min_count=1, sg=1, epochs=10)
print('Word2Vec model trained.')

#save model
os.makedirs('../model', exist_ok=True)
model.save('../model/word2vec_model.model')
print('Model saved.')