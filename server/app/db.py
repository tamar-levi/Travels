import pymysql
from app.config import DB_CONFIG


def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )


def create_users_table_if_not_exists():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            city VARCHAR(100),
            phone VARCHAR(20),
            password VARCHAR(255) NOT NULL
        )
        """

        cursor.execute(create_table_query)
        connection.commit()

        cursor.close()
        connection.close()
        print("Users table checked/created successfully.")
    except Exception as e:
        print(f"Error creating users table: {e}")


def create_travels_table_if_not_exists():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS travels (
            id INT AUTO_INCREMENT PRIMARY KEY,
            source VARCHAR(255),
            destination VARCHAR(255),
            tripDate DATE,
            tripTime TIME,
            vehicleType VARCHAR(255),
            seats INT,
            isVolunteer VARCHAR(255),
            price DECIMAL(10, 2),
            driverId INT,
            FOREIGN KEY (driverId) REFERENCES users(id)
        )
        """

        cursor.execute(create_table_query)
        connection.commit()

        cursor.close()
        connection.close()
        print("Travels table checked/created successfully.")
    except Exception as e:
        print(f"Error creating travels table: {e}")