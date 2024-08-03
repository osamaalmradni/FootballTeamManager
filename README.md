Football Team Manager
Welcome to the Football Team Manager! This application helps you manage a football team, including registering users, logging in, viewing team details, and managing user profiles.
Features
•	User Registration: Register new users with details such as username, password, first name, last name, date of birth, position, and photo.
•	User Login: Login with a registered username and password.
•	View Team: View the details of all registered users in the team.
•	Profile Management: View and update user profiles, including uploading new photos.
•	Account Deletion: Delete user accounts.
Installation
1.	Clone the repository from GitHub:
bash
Code kopieren
git clone https://github.com/osamaalmradni/FootballTeamManager.git
2.	Navigate to the project directory:
bash
Code kopieren
cd o.almaradni
3.	Install the required Python packages:
bash
Code kopieren
pip install -r requirements.txt
4.	Set up the MySQL database by executing the following SQL script:
sql
Code kopieren
CREATE DATABASE football_team;

USE football_team;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    position ENUM('Player', 'Coach') NOT NULL,
    email VARCHAR(255),
    jersey_number INT,
    street VARCHAR(255),
    building_number VARCHAR(50),
    postal_code VARCHAR(50),
    city VARCHAR(50),
    primary_position VARCHAR(50),
    secondary_position VARCHAR(50),
    height DOUBLE,
    preferred_foot VARCHAR(50),
    photo LONGBLOB
);
Usage
1.	Run the application:
bash
Code kopieren
python main.py
The main window will open, allowing you to register, login, view the team, or exit the application.
2.	To register a new user, click on the "Register" button and fill out the registration form. You can also upload a photo.
3.	To login, click on the "Login" button and enter your username and password.
4.	Once logged in, you can view and update your profile, including uploading a new photo.
5.	To view the entire team, click on the "View Team" button. The team details will be displayed in a table.
Dependencies
•	tkinter: For creating the GUI.
•	tkcalendar: For date entry widget.
•	mysql-connector-python: For connecting to the MySQL database.
•	Pillow: For handling images.
•	bcrypt: For hashing passwords.
License This project is licensed under the MIT License.
Author Osama Almaradni
GitHub: osamaalmradni
Feel free to contribute to this project by submitting issues or pull requests on GitHub. Enjoy managing your football team!
Note: Ensure that the MySQL server is running and properly configured before running the application. Adjust the MySQL connection parameters in the code if necessary.


