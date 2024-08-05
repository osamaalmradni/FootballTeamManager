# model.py

import mysql.connector
import bcrypt



class FootballTeamModel:
    """
    The Model component of the Football Team Manager application.
    Handles all database operations and data manipulation.
    """

    def __init__(self):
        """
        Initialize the model by establishing a database connection.
        """
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="football_team"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            raise Exception(f"Could not connect to database: {err}")

    def close_connection(self):
        """
        Close the database connection.
        """
        self.db.close()

    def register_user(self, username, password, first_name, last_name, dob, position):
        """
        Register a new user in the database.

        Args:
            username (str): User's username
            password (str): User's password
            first_name (str): User's first name
            last_name (str): User's last name
            dob (str): User's date of birth
            position (str): User's position

        Returns:
            bool: True if registration successful, False otherwise
        """
        try:
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            self.cursor.execute("SELECT id FROM users ORDER BY id")
            used_ids = set(id for (id,) in self.cursor.fetchall())

            first_available_id = 1
            while first_available_id in used_ids:
                first_available_id += 1

            query = """INSERT INTO users 
                    (id, username, password, first_name, last_name, date_of_birth, position) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (first_available_id, username, hashed_password, first_name, last_name, dob, position))
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Could not register user: {err}")
            return False

    def verify_user(self, username, password):
        """
        Verify user credentials.

        Args:
            username (str): User's username
            password (str): User's password

        Returns:
            int or None: User ID if verification successful, None otherwise
        """
        try:
            query = "SELECT id, password FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                return result[0]
            return None
        except mysql.connector.Error as err:
            print(f"Could not verify user: {err}")
            return None

    def get_user_data(self, user_id):
        """
        Fetch user data from the database.

        Args:
            user_id (int): User's ID

        Returns:
            tuple or None: User data if found, None otherwise
        """
        query = """SELECT username, first_name, last_name, date_of_birth, position, 
                email, street, building_number, postal_code, city, jersey_number,
                primary_position, secondary_position, height, preferred_foot
                FROM users WHERE id = %s"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def update_user_profile(self, user_id, user_data):
        """
        Update user profile in the database.

        Args:
            user_id (int): User's ID
            user_data (list): Updated user data

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            query = """UPDATE users SET username=%s, first_name=%s, last_name=%s, date_of_birth=%s, 
                    position=%s, email=%s, street=%s, building_number=%s, 
                    postal_code=%s, city=%s,jersey_number=%s, primary_position=%s, secondary_position=%s, 
                    height=%s, preferred_foot=%s WHERE id=%s"""
            
            update_data = user_data + [user_id]
            self.cursor.execute(query, tuple(update_data))
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Could not update profile: {err}")
            return False

    def delete_user(self, user_id):
        """
        Delete a user from the database.

        Args:
            user_id (int): User's ID

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            query = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Could not delete account: {err}")
            return False

    def get_team_data(self):
        """
        Fetch team data from the database.

        Returns:
            list: List of tuples containing team member data
        """
        query = """SELECT first_name, last_name, date_of_birth, position, email,  
                        street, building_number, postal_code, city, jersey_number, primary_position, secondary_position, 
                        height, preferred_foot 
                FROM users 
                ORDER BY CASE WHEN position='Coach' THEN 0 ELSE 1 END, last_name"""
        self.cursor.execute(query)
        return self.cursor.fetchall()