from src.database.mysql_connection import create_connection
import mysql.connector

def save_message_db(user_id, session_id, user_role, content):
    conn = create_connection()
    if not conn:
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO chat_history (user_id, session_id, user_role, content) 
            VALUES (%s, %s, %s, %s)""", (user_id, session_id, user_role, content))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"\n(DAO) Erro ao salvar mensagem: {e}")
        return False

def search_history_db(session_id):
    conn = create_connection()
    api_history = []

    if not conn:
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return api_history
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_role, content FROM chat_history WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
        lines = cursor.fetchall()

        for line in lines:
            api_history.append({
                "role": line["user_role"],
                "content": line["content"]
            })

        cursor.close()
        conn.close()
        return api_history
    except mysql.connector.Error as e:
        print(f"(DAO) Erro ao buscar histórico: {e}")
        return api_history