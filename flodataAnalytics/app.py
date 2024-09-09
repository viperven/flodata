# run.py

from app import app, socketio
from flask import render_template

@app.route('/')
def index():
    return render_template('auth-login-basic.html')  # Serve index.html from the templates folder

@app.route('/index')
def login_page():
    return render_template('index.html')

@app.route('/delivery')
def delivery_page():
    return render_template('delivery.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
