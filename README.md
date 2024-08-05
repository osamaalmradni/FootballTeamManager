# Football Team Manager

A comprehensive Football Team Management application developed by Mohammad Osama Almaradni.

## Description

This application provides a user-friendly interface for managing a football team. It allows users to register, login, view and edit their profiles, and view the entire team roster. The application is built using Python with Tkinter for the GUI and MySQL for data storage.

## Features

- User Registration
- User Login
- Profile Management
- Team Roster View
- Data Persistence using MySQL

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/osamaalmradni/football-team-manager.git
   ```

2. Install the required Python packages:
   ```
   pip install mysql-connector-python bcrypt tkcalendar
   ```

3. Set up the MySQL database:
   - Install MySQL if you haven't already
   - Create a new database named `football_team`
   - Use the following SQL code to create the necessary table:

   ```sql
   CREATE TABLE users (
       id INT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       date_of_birth DATE NOT NULL,
       position VARCHAR(20) NOT NULL,
       email VARCHAR(100),
       street VARCHAR(100),
       building_number VARCHAR(20),
       postal_code VARCHAR(20),
       city VARCHAR(50),
       jersey_number INT,
       primary_position VARCHAR(20),
       secondary_position VARCHAR(20),
       height INT,
       preferred_foot VARCHAR(10)
   );
   ```

4. Update the database connection details in `model.py` if necessary.

## Usage

Run the application by executing:

```
python controller.py
```

## Structure

- `controller.py`: Contains the main application logic and handles communication between the model and view.
- `model.py`: Manages database operations and data manipulation.
- `view.py`: Handles all GUI-related operations and user interactions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

Mohammad Osama Almaradni

GitHub: [https://github.com/osamaalmradni](https://github.com/osamaalmradni)

