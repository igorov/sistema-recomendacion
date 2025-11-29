from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'collaborative-filtering-secret-key-2024'

# Configuración del backend API
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5001')

@app.route('/')
def index():
    """Página de inicio - Redirect a login si no hay sesión"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Pantalla de login - Ingresar ID de usuario"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        
        if not user_id:
            flash('Por favor ingresa un ID de usuario', 'error')
            return render_template('login.html')
        
        try:
            user_id = int(user_id)
        except ValueError:
            flash('El ID de usuario debe ser un número', 'error')
            return render_template('login.html')
        
        # Validar que el usuario existe
        try:
            response = requests.get(f'{BACKEND_URL}/user/{user_id}/validate', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('exists'):
                    session['user_id'] = user_id
                    flash(f'Bienvenido Usuario {user_id}!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Usuario {user_id} no encontrado en el sistema', 'error')
            else:
                flash('Error al validar usuario', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Error de conexión con el backend: {str(e)}', 'error')
        
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/home')
def home():
    """Pantalla principal - Mostrar recomendaciones"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    recommendations = []
    history = []
    error = None
    
    try:
        # Obtener recomendaciones
        rec_response = requests.get(
            f'{BACKEND_URL}/recommendations/{user_id}',
            params={'top_k': 12},
            timeout=10
        )
        
        if rec_response.status_code == 200:
            recommendations = rec_response.json().get('recommendations', [])
        else:
            error = 'Error al obtener recomendaciones'
        
        # Obtener historial de usuario
        hist_response = requests.get(
            f'{BACKEND_URL}/user/{user_id}/history',
            params={'top_k': 6},
            timeout=10
        )
        
        if hist_response.status_code == 200:
            history = hist_response.json().get('history', [])
        
    except requests.exceptions.RequestException as e:
        error = f'Error de conexión con el backend: {str(e)}'
    
    return render_template('home.html',
                         user_id=user_id,
                         recommendations=recommendations,
                         history=history,
                         error=error)

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('user_id', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/change_user')
def change_user():
    """Cambiar de usuario"""
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
