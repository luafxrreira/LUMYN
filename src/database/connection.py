import os, mysql.connector
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    connect = None
    try:
        connect = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            port = int(os.getenv("DB_PORT", 3306))
        )

        cursor = connect.cursor()
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()
        print(f"Banco de dados conectado com sucesso: {db_version[0]}")
        cursor.close()
        return connect
    
    except mysql.connector.Error as e:
        print(f"Erro ao tentar conectar com o banco de dados. Erro: {e}")
        return None

if __name__ == "__main__":
    connection = create_connection()

