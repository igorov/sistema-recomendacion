from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import CollaborativeFilteringRecommender
import os

app = Flask(__name__)
CORS(app)

# Inicializar recomendador
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../notebooks')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

recommender = CollaborativeFilteringRecommender(DATA_PATH)

# Variable para verificar si el modelo está cargado
model_loaded = False

def init_model():
    """Inicializar o cargar modelo"""
    global model_loaded
    
    if os.path.exists(MODEL_PATH):
        print("Cargando modelo existente...")
        recommender.load_data()
        recommender.load_model(MODEL_PATH)
        model_loaded = True
    else:
        print("Entrenando nuevo modelo...")
        recommender.load_data()
        recommender.create_user_item_matrix()
        recommender.train_model(n_components=50)
        recommender.save_model(MODEL_PATH)
        model_loaded = True
    
    print("Modelo listo!")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model_loaded
    })

@app.route('/users', methods=['GET'])
def get_users():
    """Obtener lista de usuarios"""
    if not model_loaded:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    try:
        users = recommender.get_all_users()
        return jsonify({
            'users': users,
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Obtener recomendaciones para un usuario"""
    if not model_loaded:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    try:
        top_k = request.args.get('top_k', default=10, type=int)
        recommendations, status = recommender.get_recommendations(user_id, top_k=top_k)
        
        if recommendations is None:
            return jsonify({'error': status}), 404
        
        return jsonify({
            'user_id': user_id,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Obtener historial de reproducción de un usuario"""
    if not model_loaded:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    try:
        top_k = request.args.get('top_k', default=10, type=int)
        history, status = recommender.get_user_history(user_id, top_k=top_k)
        
        if history is None:
            return jsonify({'error': status}), 404
        
        return jsonify({
            'user_id': user_id,
            'history': history,
            'total': len(history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/validate', methods=['GET'])
def validate_user(user_id):
    """Validar si un usuario existe"""
    if not model_loaded:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    try:
        users = recommender.get_all_users()
        exists = user_id in users
        
        return jsonify({
            'user_id': user_id,
            'exists': exists
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_model()
    app.run(host='0.0.0.0', port=5001, debug=True)
