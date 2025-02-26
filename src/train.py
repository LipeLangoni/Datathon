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

# Baixar o arquivo ZIP
gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

# Definir o diretório de extração
extract_path = "challenge-webmedia-e-globo-2023"
os.makedirs(extract_path, exist_ok=True)  # Criar a pasta se não existir

# Extrair o ZIP dentro da pasta especificada
with zipfile.ZipFile(output_file, "r") as zip_ref:
    zip_ref.extractall(extract_path)

# Caminhos para os arquivos de treino e itens
train_files = sorted(glob.glob("challenge-webmedia-e-globo-2023/files/treino/treino_parte*.csv"))
item_files = sorted(glob.glob("challenge-webmedia-e-globo-2023/itens/itens/itens-parte*.csv"))

# Ler e concatenar os arquivos de treino
df_train = pd.concat([pd.read_csv(file) for file in train_files], ignore_index=True)

# Ler e concatenar os arquivos de itens
df_items = pd.concat([pd.read_csv(file) for file in item_files], ignore_index=True)

# Criar um ranking de popularidade baseado no número de cliques
popular_articles = df_train["history"].str.split(", ").explode().value_counts().index.tolist()

stop = stopwords.words("portuguese")

vectorizer = TfidfVectorizer(stop_words=stop)
tfidf_matrix = vectorizer.fit_transform(df_items['title'] + " " + df_items['body'])
doc_indices = {page: idx for idx, page in enumerate(df_items['page'])}

# Salvar TF-IDF Vectorizer
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Salvar Matriz TF-IDF
joblib.dump(tfidf_matrix, "tfidf_matrix.pkl")

# Salvar Dicionário de Índices
with open("doc_indices.pkl", "wb") as f:
    pickle.dump(doc_indices, f)
