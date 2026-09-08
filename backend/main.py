from flask import Flask
from dotenv import load_dotenv

from src.config.config import get_api_key
from src.database.mysql_connection import create_connection
from src.controllers.chat_controller import chat
from src.controllers.metrics_controller import metrics

load_dotenv()

app = Flask(__name__)

get_api_key()
create_connection()

app.register_blueprint(chat, url_prefix='/chat')
app.register_blueprint(metrics, url_prefix='/metrics')

if __name__ == "__main__":
    try:
        print("Servidor Flask inicializado com sucesso!")
        app.run(debug=True, port=5001, host="0.0.0.0") 
    except Exception as e:
        print(f"\nErro no servidor Flask. Erro: {e}")