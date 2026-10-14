
from pathlib import Path
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

st.set_page_config(
    page_title="Dashboard de Temperaturas IoT",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ Dashboard de Temperaturas IoT")
st.caption("Análise de 97.606 leituras de sensores de temperatura")

@st.cache_data
def load_data(view_name):
    allowed_views = {
        "avg_temp_por_dispositivo",
        "leituras_por_hora",
        "temp_max_min_por_dia"
    }
    if view_name not in allowed_views:
        raise ValueError("View não permitida")
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

try:
    # Indicadores gerais
    resumo = pd.read_sql("""
        SELECT
            COUNT(*) AS total_leituras,
            ROUND(AVG(temperature)::numeric, 2) AS temperatura_media,
            MIN(temperature) AS temperatura_minima,
            MAX(temperature) AS temperatura_maxima
        FROM temperature_readings
    """, engine)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de leituras", f"{resumo.iloc[0]['total_leituras']:,}".replace(",", "."))
    c2.metric("Temperatura média", f"{resumo.iloc[0]['temperatura_media']} °C")
    c3.metric("Temperatura mínima", f"{resumo.iloc[0]['temperatura_minima']} °C")
    c4.metric("Temperatura máxima", f"{resumo.iloc[0]['temperatura_maxima']} °C")

    st.divider()

    # Gráfico 1
    st.subheader("1. Temperatura média por dispositivo")
    df_media = load_data("avg_temp_por_dispositivo")
    fig1 = px.bar(
        df_media,
        x="device_id",
        y="avg_temp",
        labels={"device_id": "Dispositivo", "avg_temp": "Temperatura média (°C)"},
        title="Média de temperatura por dispositivo"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2
    st.subheader("2. Quantidade de leituras por hora")
    df_hora = load_data("leituras_por_hora")
    fig2 = px.line(
        df_hora,
        x="hora",
        y="contagem",
        markers=True,
        labels={"hora": "Hora do dia", "contagem": "Quantidade de leituras"},
        title="Distribuição das leituras ao longo do dia"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3
    st.subheader("3. Temperaturas máximas e mínimas por dia")
    df_diario = load_data("temp_max_min_por_dia")
    fig3 = px.line(
        df_diario,
        x="data",
        y=["temp_max", "temp_min"],
        labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Métrica"},
        title="Variação diária das temperaturas"
    )
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
