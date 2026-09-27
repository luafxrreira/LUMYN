import pandas as pd
import dotenv, os, mysql.connector

dotenv.load_dotenv()
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT")
}
conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()
if conn.is_connected():
    print("Conexão com o banco de dados estabelecida com sucesso!")

query = "SELECT * FROM rag_metrics"
df = pd.read_sql(query, conn)

cursor.close()
conn.close()

df['created_at'] = pd.to_datetime(df['created_at'])

df['response_time_s'] = df['response_time_ms'] / 1000
df['vector_search_time_s'] = df['vector_search_time_ms'] / 1000

df['status_latencia'] = df['response_time_s'].apply(lambda x: 'LENTA' if x > 5 else 'NORMAL')

diary_results = df.groupby(df['created_at'].dt.date).agg(
    total_sessions=('session_id', 'count'),
    avg_response_time=('response_time_s', 'mean'),
    avg_vector_search_time=('vector_search_time_s', 'mean'),
    total_prompt_tokens=('total_tokens', 'sum'),
    feedback_count=('feedback_user', lambda x: (x == 'like').sum())
).reset_index()

diary_results.to_csv('diary_results.csv', index=False)