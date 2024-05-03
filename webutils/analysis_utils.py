# functions to perform various NLP analyses on documents
import os
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_tfidf(tokenized_corpus, folder_path):
    # Prepare documents and file names from the tokenized corpus
    documents = [' '.join(doc) for doc in tokenized_corpus]
    file_names = os.listdir(folder_path)
    
    # Calculate TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    # Create a list of dictionaries containing filename and top 5 TF-IDF words
    result = []
    for i, filename in enumerate(file_names):
        tfidf_scores = list(zip(feature_names, tfidf_matrix[i].toarray().flatten()))
        tfidf_scores.sort(key=lambda x: x[1], reverse=True)
        top_tfidf_words = [word for word, score in tfidf_scores[:5]]
        result.append({'Filename': filename, 'Top 5 TF-IDF Words': top_tfidf_words})

    return result




