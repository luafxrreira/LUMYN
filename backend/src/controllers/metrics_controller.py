from flask import Blueprint, jsonify, request
from src.dao.metrics_dao import search_rag_metrics_db, update_feedback_user_db

metrics = Blueprint('metrics', __name__, url_prefix='/metrics')

@metrics.route('/<session_id>', methods=['GET'])
def get_metrics(session_id):
    metrics = search_rag_metrics_db(session_id)
    if metrics:
        return jsonify(metrics), 200
    else:
        return jsonify({"error": "Métricas não encontradas"}), 404

@metrics.route('/feedback', methods=['POST'])
def save_feedback():
    data = request.get_json()
    session_id = data.get('session_id')
    feedback_user = data.get('feedback_user')

    if not session_id or feedback_user is None:
        return jsonify({"error": "Parâmetros obrigatórios ausentes"}), 400

    success = update_feedback_user_db(session_id, feedback_user)
    if success:
        return jsonify({"message": "Feedback salvo com sucesso"}), 200
    else:
        return jsonify({"error": "Falha ao salvar feedback"}), 500