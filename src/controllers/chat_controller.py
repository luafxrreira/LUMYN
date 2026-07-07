from flask import Blueprint, jsonify, request
from src.services.openrouter_service import send_message_api_logic
from src.dao.history_dao import save_message_db, search_history_db

chat = Blueprint('chat', __name__)

@chat.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
        
    if not data or 'query' not in data:
        return jsonify({"erro": "O campo 'query' é obrigatório no corpo da requisição."}), 400

    query = data['query'].strip()
    session_id = data.get('session_id', 'default')
    user_id = data.get('user_id', 1)
    
    if not query:
        return jsonify({"erro": "A query não pode estar vazia."}), 400

    try:
        save_message_db(user_id, session_id, "user", query)
        
        history_update = search_history_db(session_id)
        if not history_update:
            history_update = [{"role": "user", "content": query}]

        ai_response = send_message_api_logic(history_update)
        if ai_response:
            save_message_db(user_id, session_id, "assistant", ai_response)

            return jsonify({
                    "status": "sucesso",
                    "session_id": session_id,
                    "query": query,
                    "resposta": ai_response
                }), 200
        else:
            return jsonify({"erro": "Não foi possível obter uma resposta da IA no momento."}), 500
            
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

@chat.route('/history', methods=['GET'])
def get_history():
    try:
        session_id = request.args.get('session_id', 'default')
        history = search_history_db(session_id)
        if not history:
            return jsonify({"mensagem": "Histórico vazio. Por favor, inicie uma conversa.", "historico": []}), 200
            
        return jsonify({
            "status": "sucesso",
            "session_id": session_id,
            "total_mensagens": len(history),
            "historico": history
        }), 200
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar histórico: {str(e)}"}), 500    