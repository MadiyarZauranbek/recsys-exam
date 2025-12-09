import pandas as pd
import numpy as np
import random

def generate_data(num_users=100, num_items=100, num_interactions=1000):
    """
    Генерация данных v2.0: С категориями и геолокацией.
    """
    print("🔄 Генерация расширенных данных...")

    # [cite_start]1. Товары (Items) - теперь разных типов [cite: 24, 25]
    categories = ['Movie', 'Book', 'Electronics', 'Clothing']
    genres = {
        'Movie': ['Action', 'Comedy', 'Drama', 'Sci-Fi'],
        'Book': ['Fiction', 'History', 'Business', 'Biography'],
        'Electronics': ['Phone', 'Laptop', 'Accessories', 'Camera'],
        'Clothing': ['Men', 'Women', 'Sport', 'Kids']
    }
    
    items_data = []
    for i in range(1, num_items + 1):
        cat = random.choice(categories)
        genre = random.choice(genres[cat])
        items_data.append({
            'item_id': i,
            'title': f'{cat} #{i} ({genre})',
            'category': cat,
            'genre': genre,
            'price': round(random.uniform(5.0, 500.0), 2),
            # [cite_start]Фейковые темы для LDA [cite: 8]
            'topic_id': random.randint(1, 5) 
        })
    items = pd.DataFrame(items_data)

    # [cite_start]2. Пользователи (Users) - теперь с координатами [cite: 37]
    # Генерируем точки вокруг Алматы (примерно 43.2, 76.8)
    users_data = []
    for i in range(1, num_users + 1):
        users_data.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'lat': 43.2 + random.uniform(-0.1, 0.1),
            'lon': 76.8 + random.uniform(-0.1, 0.1)
        })
    users = pd.DataFrame(users_data)

    # 3. Взаимодействия (Interactions)
    interactions = pd.DataFrame({
        'user_id': [random.randint(1, num_users) for _ in range(num_interactions)],
        'item_id': [random.randint(1, num_items) for _ in range(num_interactions)],
        'rating': [random.randint(1, 5) for _ in range(num_interactions)],
        'timestamp': pd.date_range(start='2024-01-01', periods=num_interactions, freq='h')
    })
    interactions.drop_duplicates(subset=['user_id', 'item_id'], inplace=True)

    items.to_csv('items.csv', index=False)
    users.to_csv('users.csv', index=False)
    interactions.to_csv('interactions.csv', index=False)
    
    print("✅ Данные v2.0 сгенерированы (Items, Users, Interactions)")

if __name__ == "__main__":
    generate_data()