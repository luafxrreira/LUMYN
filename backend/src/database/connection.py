import os, time, mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

def create_connection(max_tentativas=10, espera_segundos=3):
    connect = None
    for tentativa in range(1, max_tentativas + 1):
        try:
            connect = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                database = os.getenv("DB_NAME"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASS"),
                port = int(os.getenv("DB_PORT", 3306))
            )

            print("Conectado ao banco com sucesso!")
            return connect
        
        except Error as e:
            print(f"Tentativa {tentativa}/{max_tentativas} falhou: {e}")
            if tentativa < max_tentativas:
                time.sleep(espera_segundos)
        
    raise RuntimeError("Não foi possível conectar ao banco após várias tentativas.")