from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import os
import random

app = FastAPI(title="RecSys API Ultimate", version="2.0")

data = {}

def load_data():
    if not os.path.exists('items.csv'):
        print("⚠️ Данные не найдены!")
        return
    data['items'] = pd.read_csv('items.csv')
    data['users'] = pd.read_csv('users.csv')
    data['interactions'] = pd.read_csv('interactions.csv')
    print("✅ Данные загружены")

@app.on_event("startup")
def startup_event():
    load_data()

# --- ОСНОВНЫЕ РЕКОМЕНДАЦИИ ---
@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, model_type: str = "A", limit: int = 5):
    """
    Возвращает рекомендации. Поддерживает A/B тестирование.
    Model A: Случайные популярные (Simple)
    Model B: Фильтрация по любимому жанру (Smart)
    """
    items = data['items']
    interactions = data['interactions']
    
    # Исключаем просмотренное
    seen = interactions[interactions['user_id'] == user_id]['item_id'].tolist()
    candidates = items[~items['item_id'].isin(seen)]
    
    recommendations = pd.DataFrame()

    if model_type == "B":
        # Логика модели B (Умная): Ищем любимый жанр
        user_hist = interactions[interactions['user_id'] == user_id].merge(items, on='item_id')
        if not user_hist.empty:
            fav_genre = user_hist['genre'].mode()[0]
            recommendations = candidates[candidates['genre'] == fav_genre]
    
    # Если Модель А или если Модель B не нашла ничего -> просто рандом
    if recommendations.empty:
        recommendations = candidates
        
    recs = recommendations.sample(n=min(limit, len(recommendations)))
    
    # Добавляем "Объяснение"
    result = recs.to_dict(orient='records')
    for item in result:
        item['explanation'] = f"Потому что вы любите {item['genre']}" if model_type == "B" else "Популярный товар"
        
    return {"user_id": user_id, "model": model_type, "recommendations": result}

# --- СТАТИСТИКА И ПРОФИЛЬ ---
@app.get("/stats/{user_id}")
def get_stats(user_id: int):
    """Данные для графиков и профиля"""
    interactions = data['interactions']
    items = data['items']
    users = data['users']
    
    user_data = users[users['user_id'] == user_id].iloc[0].to_dict()
    user_hist = interactions[interactions['user_id'] == user_id].merge(items, on='item_id')
    
    # Топ категорий
    top_genres = user_hist['genre'].value_counts().head(5).to_dict()
    
    # Координаты для карты
    location = {"lat": user_data['lat'], "lon": user_data['lon']}
    
    return {
        "user_info": user_data,
        "top_genres": top_genres,
        "location": location,
        "history_count": len(user_hist)
    }

@app.get("/items/topics")
def get_topics():
    """Данные для визуализации LDA (Темы)"""
    # Имитация распределения тем
    return {
        "topics": {
            "Topic 1 (Action)": 20, 
            "Topic 2 (Tech)": 35, 
            "Topic 3 (Drama)": 15,
            "Topic 4 (Family)": 30
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)