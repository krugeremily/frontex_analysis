# Script for performing NLP on Risk Analysis Reports

####### Imports #######
import os
import pandas as pd
from webutils.preprocessing_utils import process_pdfs, create_corpus
from webutils.analysis_utils import calculate_tfidf
from gensim.models import Word2Vec


####### Pre-Processing Data #######

# extract text from pdf, pre-process and save as txt file
#preprocessing includes removing stopwords and punctuation, lowercasing and lemmetizing
raw_data = '../data/raw_data'
preprocessed_data = '../data/preprocessed_data'
os.makedirs(preprocessed_data, exist_ok=True)

process_pdfs(raw_data, preprocessed_data)

#turn txt files into tokenized corpus
corpus = create_corpus(preprocessed_data)
print(f'{len(corpus)} documents in corpus.')

####### TF-IDF #######

# Calculate TF-IDF matrix, feature names, and file names and store in df
tfidf_scores = calculate_tfidf(corpus, preprocessed_data)
os.makedirs('../results', exist_ok=True)
tfidf_df = pd.DataFrame(tfidf_scores).to_csv('../results/tfidf.csv')

####### Most Similar Words with TF-IDF #######

#train word2vec model
model = Word2Vec(sentences=corpus, vector_size=150, window=3, min_count=1, sg=1, epochs=10)

# Find similar words to "migrant", "migration" and "refugee" using the fine-tuned model
similar_words_migration = model.wv.most_similar('migration', topn=5)
print("Similar words to 'migration':", similar_words_migration)

similar_words_migrant = model.wv.most_similar('migrant', topn=5)
print("Similar words to 'migrant':", similar_words_migrant)

similar_words_refugee = model.wv.most_similar('refugee', topn=5)
print("Similar words to 'refugee':", similar_words_refugee)

#save model
os.makedirs('../model', exist_ok=True)
model.save('../model/word2vec_model.model')