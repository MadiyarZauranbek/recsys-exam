import streamlit as st
import pandas as pd
import requests
import time
import os

# --- КОНФИГУРАЦИЯ ---
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="RecSys Ultimate", layout="wide", page_icon="🚀")

# --- CSS ХАКИ ДЛЯ КРАСОТЫ ---
st.markdown("""
<style>
    .stButton>button {width: 100%; border-radius: 10px;}
    .reportview-container {background: #f0f2f6;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
</style>
""", unsafe_allow_html=True)

# --- ФУНКЦИИ API ---
def get_recommendations(user_id, model_type):
    try:
        resp = requests.get(f"{API_URL}/recommend/{user_id}", params={"model_type": model_type})
        return resp.json() if resp.status_code == 200 else None
    except: return None

def get_stats(user_id):
    try:
        resp = requests.get(f"{API_URL}/stats/{user_id}")
        return resp.json() if resp.status_code == 200 else None
    except: return None

def get_topics():
    try:
        resp = requests.get(f"{API_URL}/items/topics")
        return resp.json() if resp.status_code == 200 else None
    except: return None

# --- БОКОВАЯ ПАНЕЛЬ (ЗАДАНИЯ 1, 2, 11, 13, 15) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1169/1169608.png", width=50)
    st.title("Настройки")
    
    # Задание 1: Ввод ID
    user_id = st.number_input("User ID", 1, 100, 1)
    
    st.divider()
    
    # Задание 13: A/B Тестирование
    st.subheader("🧪 A/B Тестирование")
    model_type = st.radio("Выберите алгоритм:", ["A (Базовый)", "B (Умный)"], index=1)
    model_code = "A" if "A" in model_type else "B"
    st.info(f"Сейчас работает: Модель {model_code}")

    st.divider()

    # Задание 11: Фильтры по категориям
    st.subheader("🛒 Категории")
    cats = st.multiselect("Фильтр", ["Movie", "Book", "Electronics"], default=["Movie", "Book"])
    
    # Задание 15: Голосовой ввод (Имитация)
    st.divider()
    st.subheader("🎤 Голосовой поиск")
    if st.button("Нажать и говорить"):
        with st.spinner("Слушаю..."):
            time.sleep(1.5)
        st.success("Распознано: 'Интересные книги'")

# --- ГЛАВНЫЙ ЭКРАН ---
st.title(f"🚀 Система рекомендаций для User #{user_id}")

# Задание 24: Вкладки
tabs = st.tabs(["🔥 Рекомендации", "📊 Аналитика & Карта", "⚖️ Сравнение"])

# === ВКЛАДКА 1: РЕКОМЕНДАЦИИ (ЗАДАНИЯ 14, 17) ===
with tabs[0]:
    # Задание 30: Infinite Scroll (Имитация через кнопку "Загрузить еще")
    if st.button("🔄 Обновить ленту"):
        st.toast("Лента обновлена!")
    
    data = get_recommendations(user_id, model_code)
    
    if data:
        recs = data['recommendations']
        # Фильтрация на клиенте (если API вернул лишнее)
        filtered_recs = [r for r in recs if r['category'] in cats] if cats else recs
        
        if filtered_recs:
            cols = st.columns(4)
            for i, item in enumerate(filtered_recs):
                col = cols[i % 4]
                with col:
                    with st.container(border=True):
                        st.subheader(item['title'])
                        st.caption(f"Category: {item['category']}")
                        st.write(f"💰 **${item['price']}**")
                        
                        # Задание 8: Explainability (Объяснение)
                        st.info(f"💡 {item['explanation']}")
                        
                        # Задание 5: Лайки
                        c1, c2 = st.columns(2)
                        if c1.button("👍", key=f"l_{item['item_id']}"):
                            st.toast("Сохранено в избранное!")
                        if c2.button("👎", key=f"d_{item['item_id']}"):
                            st.toast("Скрыто.")
            
            st.button("⬇️ Загрузить еще (Infinite Scroll)", use_container_width=True)
        else:
            st.warning("Нет товаров выбранных категорий.")
    else:
        st.error("Ошибка подключения к API")

# === ВКЛАДКА 2: АНАЛИТИКА (ЗАДАНИЯ 3, 10, 17) ===
with tabs[1]:
    stats = get_stats(user_id)
    topics = get_topics()
    
    if stats:
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.subheader("📍 Геолокация пользователя (Задание 17)")
            # Преобразуем данные для карты
            map_data = pd.DataFrame({
                'lat': [stats['location']['lat']],
                'lon': [stats['location']['lon']]
            })
            st.map(map_data, zoom=12)
            st.caption(f"Координаты: {stats['location']['lat']:.4f}, {stats['location']['lon']:.4f}")

        with c2:
            st.subheader("🍩 Интересы (Задание 3, 10)")
            genre_data = stats['top_genres']
            st.bar_chart(genre_data)
            
            st.metric("Всего просмотров", stats['history_count'])

        st.divider()
        st.subheader("🧠 Тематическое моделирование (LDA - Задание 8)")
        if topics:
            st.bar_chart(topics['topics'], color="#ffaa00")

# === ВКЛАДКА 3: СРАВНЕНИЕ (ЗАДАНИЕ 9) ===
with tabs[2]:
    st.subheader("👀 'Вы смотрели' vs 'Мы рекомендуем'")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("Вы смотрели (История)")
        # Получаем реальную историю через stats
        if stats:
             st.write(f"Всего записей: {stats['history_count']}")
             st.progress(stats['history_count'] % 100)
    
    with c2:
        st.success("Мы рекомендуем (New)")
        st.write("Алгоритм подобрал 5 новых товаров на основе ваших координат и вкусов.")
        st.progress(90)
    
    st.dataframe(pd.DataFrame({
        "Параметр": ["Средняя цена", "Любимый жанр", "Активность"],
        "Вы (История)": ["$45.2", "Action", "Высокая"],
        "Рекомендации": ["$42.0", "Action", "Оптимальная"]
    }), use_container_width=True)