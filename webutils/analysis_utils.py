# functions to perform various NLP analyses on documents
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
import math


def calculate_tfidf(tokenized_corpus, folder_path):
    #prepare documents and file names from tokenized corpus
    documents = [' '.join(doc) for doc in tokenized_corpus]
    file_names = [filename for filename in os.listdir(folder_path) if filename.endswith('.txt')]
    
    #calculate TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    #create a list of dictionaries containing filename, top 10 TF-IDF words and scores
    result = []
    for i, filename in enumerate(file_names):
        tfidf_scores = list(zip(feature_names, tfidf_matrix[i].toarray().flatten()))
        tfidf_scores.sort(key=lambda x: x[1], reverse=True)
        top_tfidf_words_with_scores = tfidf_scores[:10]
        result.append({'Filename': filename, 'Top 10 TF-IDF Words': top_tfidf_words_with_scores})

    return result

#function to compute keyness score
def compute_keyness(word, doc_freq, ref_freq, doc_size, ref_size):
    if doc_size == 0 or ref_size == 0:
        return 0
    #expected frequency
    expected_freq=(doc_size*ref_freq)/(doc_size+ref_size)
    #compute keyness score using log-likelihood ratio
    if doc_freq > expected_freq and expected_freq > 0:
        return 2*(doc_freq*math.log(doc_freq/expected_freq))
    else:
        return 0


