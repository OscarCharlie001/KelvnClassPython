from flask import blueprints, request, jsonify
from app import mongo
import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth = blueprints.Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"msg": "No input data provided, Missing Json in request"}), 400
        email = data.get('email')
        password = data.get('password')
        name=data.get('name')

        if not email or not password:
            return jsonify({"msg": "Email and password are required"}), 401
        
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            return jsonify({"msg": "User already exists"}), 409
        
        # if mongo.db.users.find_one({"email": email}):
        #     return jsonify({"msg": "User already exists"}), 409
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            "email": email,
            "password": hashed_password,
            "name": name
        }
        mongo.db.users.insert_one(user_data)

        access_token = create_access_token(identity=email, expires_delta=timedelta(days=7))

        return jsonify({"msg": "User created successfully","access_token": access_token}), 201
    
    except Exception as e:
        return jsonify({"msg": "Error during signup", "error": str(e)}), 500
