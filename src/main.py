import joblib
import numpy as np
from fastapi import FastAPI
import pickle
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import glob

class PredictionInput(BaseModel):
    user_history: list
    top_n: int

csv_files = glob.glob('challenge-webmedia-e-globo-2023/itens/itens/itens-parte*.csv')

df_items = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

df_items["timestamp"] = pd.to_datetime(df_items["issued"]).astype(int) // 10**9

with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

tfidf_matrix = joblib.load("tfidf_matrix.pkl")

with open("doc_indices.pkl", "rb") as f:
    doc_indices = pickle.load(f)

# Criar API
app = FastAPI()

class RecommendRequest(BaseModel):
    history: list
    timestampHistory: list
    recommendationSize: int = 5

@app.post("/recommend")
def recommend_news(request: RecommendRequest):
    user_history = request.history
    timestamps = request.timestampHistory
    top_n = request.recommendationSize

    if not user_history or not timestamps:
        popular_articles = df_items['page'].value_counts().head(top_n).index.tolist()
        recommendations = df_items[df_items['page'].isin(popular_articles)][['page', 'title']].to_dict(orient="records")
        return {"recommendations": recommendations}
    
    last_user_timestamp = max(timestamps)
    viewed_indices = [doc_indices[page] for page in user_history if page in doc_indices]

    if not viewed_indices:
        return {"message": "Nenhuma notícia válida encontrada no histórico.", "recommendations": []}

    
    user_profile = np.mean(tfidf_matrix[viewed_indices], axis=0)

    scores = cosine_similarity(np.asarray(user_profile), tfidf_matrix).flatten()

    valid_indices = df_items.index[df_items["page"].isin(doc_indices.keys())]

    news_timestamps = df_items.loc[valid_indices, "timestamp"].values

    time_diffs = np.abs(news_timestamps - last_user_timestamp)

    recency_factor = np.exp(-time_diffs / (7 * 24 * 3600))

    adjusted_scores = scores[valid_indices] * recency_factor

    recommended_indices = np.argsort(adjusted_scores)[::-1]
    recommended_pages = [
        df_items.iloc[i]['page'] for i in recommended_indices if df_items.iloc[i]['page'] not in user_history
    ][:top_n]

    recommendations = df_items[df_items['page'].isin(recommended_pages)][['page', 'title']].to_dict(orient="records")

    return {"recommendations": recommendations}
