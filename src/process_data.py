
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega as configurações do arquivo .env
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no arquivo .env")

# Conecta ao PostgreSQL
engine = create_engine(DATABASE_URL)

# Lê o arquivo CSV
csv_path = BASE_DIR / "data" / "IOT-temp.csv"
df = pd.read_csv(csv_path)

# Ajusta os nomes das colunas para facilitar as consultas SQL
df = df.rename(columns={
    "id": "source_id",
    "room_id/id": "device_id",
    "noted_date": "noted_date",
    "temp": "temperature",
    "out/in": "location_type"
})

# Converte os dados para os tipos corretos
df["noted_date"] = pd.to_datetime(
    df["noted_date"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)
df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")

# Remove linhas inválidas
df = df.dropna(subset=["noted_date", "temperature", "device_id"])

# Cria a tabela e importa os dados em lotes
with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS temperature_readings"))

    connection.execute(text("""
        CREATE TABLE temperature_readings (
            id BIGSERIAL PRIMARY KEY,
            source_id VARCHAR(100),
            device_id VARCHAR(100),
            noted_date TIMESTAMP,
            temperature DOUBLE PRECISION,
            location_type VARCHAR(10)
        )
    """))

with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE temperature_readings"))

    df.to_sql(
        "temperature_readings",
        connection,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

print(f"Importação concluída: {len(df)} registros processados.")
