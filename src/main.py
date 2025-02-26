from tensorflow.keras.models import load_model
import joblib
import json
import requests
import numpy as np
from fastapi import FastAPI
import pickle
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class PredictionInput(BaseModel):
    user_history: list
    top_n: int

df_train = pd.read_csv(f'challenge-webmedia-e-globo-2023/files/treino/treino_parte1.csv')
df_items = pd.read_csv(f'challenge-webmedia-e-globo-2023/itens/itens/itens-parte1.csv')

# Converter timestamps para segundos
df_items["timestamp"] = pd.to_datetime(df_items["issued"]).astype(int) // 10**9

# Carregar modelos salvos
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

tfidf_matrix = joblib.load("tfidf_matrix.pkl")

with open("doc_indices.pkl", "rb") as f:
    doc_indices = pickle.load(f)

# Criar API
app = FastAPI()

class RecommendRequest(BaseModel):
    history: list
    timestampHistory_new: list  # Lista de timestamps das interações do usuário
    top_n: int = 5

@app.post("/recommend")
def recommend_news(request: RecommendRequest):
    user_history = request.history
    timestamps = request.timestampHistory_new
    top_n = request.top_n

    if not user_history or not timestamps:
        return {"message": "Histórico ou timestamps vazios.", "recommendations": []}

    last_user_timestamp = max(timestamps)
    viewed_indices = [doc_indices[page] for page in user_history if page in doc_indices]

    if not viewed_indices:
        return {"message": "Nenhuma notícia válida encontrada no histórico.", "recommendations": []}

    user_profile = np.mean(tfidf_matrix[viewed_indices], axis=0)

    scores = cosine_similarity(np.asarray(user_profile), tfidf_matrix).flatten()

    news_timestamps = df_items["timestamp"].values
    time_diffs = np.abs(news_timestamps - last_user_timestamp)  # Diferença de tempo em segundos
    recency_factor = np.exp(-time_diffs / (7 * 24 * 3600))  # Decaimento para 7 dias

    # Ajustar scores com a recência
    adjusted_scores = scores * recency_factor

    # Obter as top-N notícias mais relevantes e recentes
    recommended_indices = np.argsort(adjusted_scores)[::-1]
    recommended_pages = [
        df_items.iloc[i]['page'] for i in recommended_indices if df_items.iloc[i]['page'] not in user_history
    ][:top_n]

    recommendations = df_items[df_items['page'].isin(recommended_pages)][['page', 'title']].to_dict(orient="records")

    return {"recommendations": recommendations}
