import bcrypt
from flask import Blueprint, request, jsonify
from pymysql.cursors import DictCursor
from app.auth.passwords import hash_password
from app.db import get_db_connection
from app.auth.token import encode_auth_token, decode_auth_token
import logging
logging.basicConfig(level = logging.DEBUG)
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/addUser', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        city = data['city']
        phone = data['phone']
        password = data['password']

        hashed_password = hash_password(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({"error": "Email already exists"}), 400

        cursor.execute(
            "INSERT INTO users (name, email, city, phone, password) VALUES (%s, %s, %s, %s, %s)",
            (name, email, city, phone, hashed_password),
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "User added successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500



@auth_bp.route('/getUser', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        name = data['name']
        password = data['password']

        connection = get_db_connection()
        cursor = connection.cursor(DictCursor)

        cursor.execute(
            "SELECT * FROM users WHERE name = %s",
            (name,)
        )
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            stored_hashed_password = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                user_id = user['id']
                token = encode_auth_token(user_id)
                return jsonify({"message": "User found", "token": token}), 200
            else:
                return jsonify({"message": "Invalid password"}), 401
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@auth_bp.route('/getCurrentUserDetails', methods=['GET'])
def get_current_user_details():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header is missing or invalid'}), 401

    token = auth_header.split(' ')[1]

    user_id = decode_auth_token(token)
    if isinstance(user_id, str) and user_id.startswith('Invalid'):
        return jsonify({'error': user_id}), 401

    connection = get_db_connection()
    cursor = connection.cursor(DictCursor)

    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_details = cursor.fetchone()

        if not user_details:
            return jsonify({'error': 'User not found'}), 404

        if 'password' in user_details:
            del user_details['password']

        return jsonify(user_details), 200

    except Exception as e:
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

