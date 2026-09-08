from src.database.mysql_connection import create_connection

def save_rag_metrics_db(session_id, response_time_ms, prompt_tokens, completion_tokens, total_tokens, vector_search_time_ms=None, feedback_user=None):
    conn = create_connection()
    if not conn: 
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO rag_metrics (session_id, response_time_ms, prompt_tokens, completion_tokens, total_tokens, vector_search_time_ms, feedback_user) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
            (session_id, response_time_ms, prompt_tokens, completion_tokens, total_tokens, vector_search_time_ms, feedback_user))
        conn.commit()
        return True
    except Exception as e:
        print(f"\n(DAO) Erro ao salvar métricas RAG: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_rag_metrics_db(session_id):
    conn = create_connection()
    metrics = {}

    if not conn:
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return metrics
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rag_metrics WHERE session_id = %s", (session_id,))
        line = cursor.fetchone()

        if line:
            metrics = {
                "session_id": line["session_id"],
                "response_time_ms": line["response_time_ms"],
                "prompt_tokens": line["prompt_tokens"],
                "completion_tokens": line["completion_tokens"],
                "total_tokens": line["total_tokens"],
                "vector_search_time_ms": line["vector_search_time_ms"],
                "feedback_user": line["feedback_user"]
            }

        return metrics
    except Exception as e:
        print(f"(DAO) Erro ao buscar métricas RAG: {e}")
        return metrics
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_feedback_user_db(session_id, feedback_user):
    conn = create_connection()
    if not conn:
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE rag_metrics SET feedback_user = %s WHERE session_id = %s", (feedback_user, session_id))
        conn.commit()

        return True
    except Exception as e:
        print(f"(DAO) Erro ao atualizar feedback do usuário: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_rag_metrics_db(session_id):
    conn = create_connection()
    if not conn:
        print("(DAO) Erro: Não foi possível estabelecer conexão com o banco.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rag_metrics WHERE session_id = %s", (session_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"(DAO) Erro ao deletar métricas RAG: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()