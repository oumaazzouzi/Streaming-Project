from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATA_FILE = 'data/user_events.csv'

# Création du dossier et fichier
os.makedirs('data', exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password', 'event_type', 'content', 'timestamp'])

# Fonction pour enregistrer un événement (avec ou sans mot de passe selon le cas)
def enregistrer_evenement(username, password='', event_type='', content=''):
    timestamp = datetime.now().isoformat()
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, event_type, content, timestamp])

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        enregistrer_evenement(username, password, 'register', 'Register')
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(DATA_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    session['username'] = username
                    session['show_welcome'] = True
                    enregistrer_evenement(username, '', 'login', 'Login')
                    return redirect(url_for('dashboard'))
        return render_template('login.html', error="Identifiants invalides.")
    return render_template('login.html')

# Tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    show_welcome = session.pop('show_welcome', False)
    return render_template('dashboard.html', username=session['username'], show_welcome=show_welcome)

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Enregistrement d'événements JS
@app.route('/log_event', methods=['POST'])
def log_event():
    data = request.get_json()
    if not all(k in data for k in ('user_id', 'content', 'event_type')):
        return jsonify({'status': 'error', 'message': 'Données manquantes'}), 400

    enregistrer_evenement(data['user_id'], '', data['event_type'], data['content'])
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
