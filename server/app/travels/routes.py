import logging
from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.auth.token import decode_auth_token
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)

travels_bp = Blueprint('travels', __name__)

@travels_bp.route('/addTravel', methods=['POST'])
def add_travel():
    try:
        logging.debug("Received request to add travel")

        token = request.headers.get('Authorization')
        logging.debug(f"Token from request headers: {token}")

        if not token:
            logging.error("Token is missing in request")
            return jsonify({"error": "Token is missing"}), 401

        token = token.split(" ")[1] if "Bearer" in token else None
        logging.debug(f"Extracted token: {token}")

        if not token:
            logging.error("Token is invalid or missing after extraction")
            return jsonify({"error": "Token is invalid"}), 401

        user_id = decode_auth_token(token)
        logging.debug(f"Decoded user_id: {user_id}")

        try:
            user_id = int(user_id)
        except ValueError:
            logging.error(f"Error decoding token: {user_id}")
            return jsonify({"error": "Invalid token or user_id"}), 401

        data = request.get_json()
        logging.debug(f"Request data: {data}")

        source = data['source']
        destination = data['destination']
        tripDate = data['tripDate']
        tripTime = data['tripTime']
        vehicleType = data['vehicleType']
        seats = data['seats']
        isVolunteer = data['isVolunteer']
        price = data['price']
        try:
            driverId = int(user_id)
        except ValueError:
            logging.error("Invalid user_id format, unable to convert to INT")
            return jsonify({"error": "Invalid token format"}), 401

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO travels (source, destination, tripDate, tripTime, vehicleType, seats, isVolunteer, price, driverId) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (source, destination, tripDate, tripTime, vehicleType, seats, isVolunteer, price, driverId))
        logging.debug(f"Data inserted: {source}, {destination}, {tripDate}, {tripTime}, {vehicleType}, {seats}, "
                      f"{isVolunteer}, {price}, {driverId}")

        connection.commit()
        cursor.close()
        connection.close()

        logging.debug("Travel added successfully")
        return jsonify({"message": "Travel added successfully"}), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@travels_bp.route('/getAllTravels', methods=['GET'])
def get_all_travels():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM travels""")
        travels = cursor.fetchall()

        result = []
        for travel in travels:
            travel_dict = {
                'travel_id': travel[0],
                'startPoint': travel[1],
                'endPoint': travel[2],
                'date': travel[3],
                'time': travel[4],
                'vehicleType': travel[5],
                'seatsAvailable': travel[6],
                'cost': travel[8]
            }

            if isinstance(travel[4], timedelta):
                time = travel[4]
                days = time.days
                hours, remainder = divmod(time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                formatted_time = f"{days} days {hours} hours {minutes} minutes"
                travel_dict['time'] = formatted_time

            driver_id = travel[9]
            cursor.execute("SELECT name, email, phone FROM users WHERE id = %s", (driver_id,))
            driver = cursor.fetchone()

            if driver:
                travel_dict['driverName'] = driver[0]
                travel_dict['driverEmail'] = driver[1]
                travel_dict['driverPhone'] = driver[2]
            else:
                travel_dict['driverName'] = None
                travel_dict['driverEmail'] = None
                travel_dict['driverPhone'] = None

            result.append(travel_dict)

        cursor.close()
        connection.close()

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
