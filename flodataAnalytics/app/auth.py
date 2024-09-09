# app/auth.py

from flask import jsonify, request, session,make_response
from app import app
from .models import get_user_by_email
from werkzeug.security import check_password_hash
import uuid  # For generating a unique order number

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    if not all([email, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['user_id']
        session['role'] = user['role']
         # On success:
        response = make_response(jsonify({'success': True, 'token': 'your_auth_token_here'}))
        response.set_cookie('authToken', 'your_auth_token_here', httponly=True)
        return jsonify({'message': 'Login successful', 'success': True}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401

@app.route('/protected')
def protected():
    auth_token = request.cookies.get('authToken')
    if auth_token == 'your_auth_token_here':  # Validate the token
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({'message': 'Logout successful'}), 200





