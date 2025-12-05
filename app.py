import streamlit as st
import pandas as pd
import requests

import os

# --- КОНФИГУРАЦИЯ ---
# Если переменная окружения задана (в Docker), используем её.
# Если нет (локальный запуск), используем 127.0.0.1
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="RecSys Interface (API)", layout="wide")

# --- ФУНКЦИИ ЗАПРОСОВ К API ---
def get_recommendations(user_id):
    """Запрашивает рекомендации у API"""
    try:
        response = requests.get(f"{API_URL}/recommend/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка API: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("🚨 Ошибка подключения! Убедитесь, что API (api.py) запущен.")
        return None

def get_history(user_id):
    """Запрашивает историю у API"""
    try:
        response = requests.get(f"{API_URL}/history/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data['history'])
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- ИНТЕРФЕЙС ---
st.title("🎥 Система рекомендаций (Client-Server)")

# Боковая панель
user_id = st.sidebar.number_input("Введите User ID", min_value=1, value=1)

# Кнопка обновления
if st.sidebar.button("Получить рекомендации"):
    # 1. Запрос к API
    with st.spinner('Стучимся к серверу...'):
        data = get_recommendations(user_id)
    
    if data and data['recommendations']:
        st.success(f"Получено {len(data['recommendations'])} рекомендаций от API")
        
        # Отображение карточек
        cols = st.columns(len(data['recommendations']))
        for idx, item in enumerate(data['recommendations']):
            with cols[idx]:
                st.info(f"**{item['title']}**")
                st.caption(f"{item['genre']} | ${item['price']}")
                st.button("👍", key=f"btn_{item['item_id']}")
    else:
        st.warning("API не вернул рекомендаций или пользователь новый.")

# Блок истории (Загружается всегда)
st.divider()
st.subheader("👤 Профиль пользователя (из API)")
history_df = get_history(user_id)

if not history_df.empty:
    st.dataframe(history_df, width=1000)
else:
    st.info("История пуста или API недоступен.")