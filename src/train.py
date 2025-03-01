import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import glob
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pickle
import joblib
import gdown
import zipfile
import os
file_id = "13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr"
output_file = "challenge-webmedia-e-globo-2023.zip"


gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

extract_path = "challenge-webmedia-e-globo-2023"
os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(output_file, "r") as zip_ref:
    zip_ref.extractall(extract_path)

train_files = sorted(glob.glob("challenge-webmedia-e-globo-2023/files/treino/treino_parte*.csv"))
item_files = sorted(glob.glob("challenge-webmedia-e-globo-2023/itens/itens/itens-parte*.csv"))

df_train = pd.concat([pd.read_csv(file) for file in train_files], ignore_index=True)

df_items = pd.concat([pd.read_csv(file) for file in item_files], ignore_index=True)

popular_articles = df_train["history"].str.split(", ").explode().value_counts().index.tolist()

stop = stopwords.words("portuguese")

vectorizer = TfidfVectorizer(stop_words=stop)
tfidf_matrix = vectorizer.fit_transform(df_items['title'] + " " + df_items['body'])
doc_indices = {page: idx for idx, page in enumerate(df_items['page'])}

with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

joblib.dump(tfidf_matrix, "tfidf_matrix.pkl")

with open("doc_indices.pkl", "wb") as f:
    pickle.dump(doc_indices, f)
