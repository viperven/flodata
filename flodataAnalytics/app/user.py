# app/user.py

from flask import jsonify, request
from app import app
from .models import add_user
from werkzeug.security import generate_password_hash

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    print("register") 

    if not all([name, email, password, role]):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(password)

    user_data = (name, email, hashed_password, role)
    print(user_data)
    try:
        add_user(user_data)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
