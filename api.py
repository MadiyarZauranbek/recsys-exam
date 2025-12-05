from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import os

# Инициализируем приложение
app = FastAPI(
    title="RecSys API",
    description="Микросервис для выдачи рекомендаций",
    version="1.0.0"
)

# Глобальные переменные для данных
data = {}

def load_data():
    """Загрузка данных в память при старте сервера"""
    if not os.path.exists('items.csv'):
        # Если данных нет, API не сможет работать корректно без генератора
        # Но для простоты считаем, что app.py их уже создал
        raise RuntimeError("Файлы данных не найдены! Сначала запустите app.py")
    
    data['items'] = pd.read_csv('items.csv')
    data['users'] = pd.read_csv('users.csv')
    data['interactions'] = pd.read_csv('interactions.csv')
    print("✅ Данные загружены в память API")

# Событие старта сервера
@app.on_event("startup")
def startup_event():
    load_data()

# --- ENDPOINTS (РУЧКИ) ---

@app.get("/")
def read_root():
    return {"status": "online", "service": "RecSys API v1"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, limit: int = 5):
    """
    Возвращает список рекомендаций для конкретного user_id.
    """
    items = data['items']
    interactions = data['interactions']

    # Проверка существования пользователя (упрощенно)
    if user_id not in data['users']['user_id'].values:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Логика исключения просмотренного
    user_history = interactions[interactions['user_id'] == user_id]['item_id'].tolist()
    candidates = items[~items['item_id'].isin(user_history)]

    if candidates.empty:
        return {"user_id": user_id, "recommendations": []}

    # Возвращаем случайные (MOCK model)
    recs = candidates.sample(n=min(limit, len(candidates)))
    
    # Превращаем в список словарей для JSON ответа
    result = recs[['item_id', 'title', 'genre', 'price']].to_dict(orient='records')
    
    return {
        "user_id": user_id,
        "count": len(result),
        "recommendations": result
    }

@app.get("/history/{user_id}")
def get_history(user_id: int):
    """
    Возвращает историю оценок пользователя
    """
    interactions = data['interactions']
    items = data['items']
    
    user_history = interactions[interactions['user_id'] == user_id].merge(items, on='item_id')
    
    if user_history.empty:
        return {"user_id": user_id, "history": []}
        
    result = user_history[['title', 'genre', 'rating', 'timestamp']].sort_values('timestamp', ascending=False).head(10).to_dict(orient='records')
    return {"user_id": user_id, "history": result}

if __name__ == "__main__":
    # Запуск сервера на порту 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)