"""Aplicación Flask - Frontend del sistema de recomendación"""
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/users', methods=['GET'])
def get_users():
    """Obtener usuarios disponibles"""
    try:
        limit = request.args.get('limit', 100, type=int)
        response = requests.get(f'{API_BASE_URL}/api/users', params={'limit': limit})
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/state', methods=['GET'])
def get_user_state(user_id):
    """Obtener estado de un usuario"""
    try:
        response = requests.get(f'{API_BASE_URL}/api/users/{user_id}/state')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': str(e)}), e.response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Obtener recomendación para un usuario"""
    try:
        data = request.json
        response = requests.post(f'{API_BASE_URL}/api/recommend', json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': str(e)}), e.response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Enviar feedback sobre una recomendación"""
    try:
        data = request.json
        response = requests.post(f'{API_BASE_URL}/api/feedback', json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': str(e)}), e.response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Obtener estadísticas del agente"""
    try:
        response = requests.get(f'{API_BASE_URL}/api/statistics')
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """Obtener perfil de un usuario"""
    try:
        response = requests.get(f'{API_BASE_URL}/api/users/{user_id}/profile')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': str(e)}), e.response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

