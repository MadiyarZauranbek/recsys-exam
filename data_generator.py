import pandas as pd
import numpy as np
import random

def generate_data(num_users=100, num_items=50, num_interactions=500):
    """
    Генерирует синтетические данные для рекомендательной системы.
    """
    # 1. Генерация товаров (фильмов/книг)
    genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror']
    items = pd.DataFrame({
        'item_id': range(1, num_items + 1),
        'title': [f'Item {i}' for i in range(1, num_items + 1)],
        'genre': [random.choice(genres) for _ in range(num_items)],
        'price': [round(random.uniform(5.0, 50.0), 2) for _ in range(num_items)]
    })

    # 2. Генерация пользователей
    users = pd.DataFrame({
        'user_id': range(1, num_users + 1),
        'age': [random.randint(18, 60) for _ in range(num_users)],
        'gender': [random.choice(['M', 'F']) for _ in range(num_users)]
    })

    # 3. Генерация взаимодействий (оценок)
    interactions = pd.DataFrame({
        'user_id': [random.randint(1, num_users) for _ in range(num_interactions)],
        'item_id': [random.randint(1, num_items) for _ in range(num_interactions)],
        'rating': [random.randint(1, 5) for _ in range(num_interactions)],
        'timestamp': pd.date_range(start='2024-01-01', periods=num_interactions, freq='H')
    })

    # Удаляем дубликаты (один юзер - один товар)
    interactions.drop_duplicates(subset=['user_id', 'item_id'], inplace=True)

    # Сохраняем
    items.to_csv('items.csv', index=False)
    users.to_csv('users.csv', index=False)
    interactions.to_csv('interactions.csv', index=False)
    
    print("✅ Данные сгенерированы: items.csv, users.csv, interactions.csv")

if __name__ == "__main__":
    generate_data()