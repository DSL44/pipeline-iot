Pipeline de Dados com IoT e Docker

1. Objetivo do projeto

O objetivo deste projeto é desenvolver um pipeline de dados capaz de processar leituras de temperatura de dispositivos IoT, armazenar os dados em um banco PostgreSQL e disponibilizar análises por meio de um dashboard interativo.

2. Tecnologias utilizadas

- Python: processamento dos dados.
- Pandas: leitura e tratamento do arquivo CSV.
- SQLAlchemy: conexão entre Python e PostgreSQL.
- PostgreSQL: armazenamento dos dados.
- Docker e Docker Compose: execução do banco de dados em um contêiner.
- Streamlit: criação do dashboard.
- Plotly: geração dos gráficos interativos.

3. Fonte dos dados

Foi utilizado o conjunto de dados "Temperature Readings: IoT Devices", disponível no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

Arquivo utilizado: data/IOT-temp.csv.

O arquivo contém 97.606 registros e cinco colunas originais: id, room_id/id, noted_date, temp e out/in.

4. Arquitetura do pipeline

O fluxo de processamento é composto pelas seguintes etapas:

1. Leitura do arquivo CSV.
2. Tratamento e conversão dos dados com Python e Pandas.
3. Armazenamento das leituras no PostgreSQL.
4. Criação de Views SQL para análise.
5. Consulta das Views pelo dashboard Streamlit.
6. Visualização dos resultados por meio de gráficos interativos.

Fluxo: CSV; Python/Pandas; PostgreSQL; Views SQL; Streamlit/Plotly.

5. Estrutura do projeto

- data/: arquivo CSV utilizado.
- src/process_data.py: processamento e importação dos dados.
- src/dashboard.py: aplicação de visualização.
- sql/views.sql: definições das três Views SQL.
- docker-compose.yml: configuração do PostgreSQL.
- .env: configuração local da conexão com o banco.
- .gitignore: arquivos que não devem ser enviados ao Git.
- requirements.txt: dependências Python.
- README.md: documentação do projeto.

6. Configuração e execução

Pré-requisitos

- Python 3.12.
- Docker Desktop.
- Git.

Instalação das dependências:

Executado na pasta principal do projeto:


pip install -r requirements.txt
pip install python-dotenv


Configuração da conexão

Crie um arquivo .env na raiz do projeto com a variável DATABASE_URL, utilizando as credenciais definidas no docker-compose.yml.

Não publique esse arquivo no GitHub.


- Inicialização do PostgreSQL:


docker compose up -d


- Processamento e importação dos dados:


python src/process_data.py


 - Criação das Views SQL:


Get-Content .\sql\views.sql | docker exec -i postgres-iot psql -U iot_user -d iot_db


- Execução do dashboard:


streamlit run src/dashboard.py


7. Views SQL
   

- avg_temp_por_dispositivo:

Calcula a temperatura média agrupada por dispositivo. Permite observar as médias registradas para cada identificador de ambiente.

- leituras_por_hora:

Conta a quantidade de leituras registradas em cada hora do dia. Permite analisar a distribuição temporal dos registros.

- temp_max_min_por_dia:

Calcula as temperaturas máxima e mínima para cada dia. Permite acompanhar a variação diária dos valores registrados.


8. Dashboard

O dashboard apresenta indicadores gerais e três visualizações:

- Temperatura média por dispositivo.
- Quantidade de leituras por hora.
- Temperaturas máximas e mínimas por dia.
  

**Captura de tela:** inserir aqui uma imagem real do dashboard em execução.


9. Resultados e possíveis aplicações
    

O pipeline demonstra como dados de sensores podem ser gerados, processados, armazenados e consultados para apoiar análises.


10. Conclusão

O projeto integra Python, Docker, PostgreSQL e Streamlit em um fluxo de dados de IoT. A solução permite armazenar leituras de temperatura, realizar consultas por meio de Views SQL e apresentar os resultados em gráficos interativos.

