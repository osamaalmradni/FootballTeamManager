# controller.py

from model import FootballTeamModel
from view import FootballTeamView
import tkinter as tk

class FootballTeamController:
    """
    The Controller component of the Football Team Manager application.
    Handles the communication between the Model and the View.
    """

    def __init__(self, root):
        """
        Initialize the controller.

        Args:
            root: The root window of the application
        """
        self.root = root
        self.model = FootballTeamModel()
        self.view = FootballTeamView(root)
        self.bind_events()

    def bind_events(self):
        """
        Bind events to the buttons in the main window.
        """
        # Ensure that you get the buttons correctly
        register_button, login_button, view_team_button, exit_button = self.view.create_main_window()

        
        # Debugging prints
        print("Buttons created")
        print(f"Register button: {register_button}")
        print(f"Login button: {login_button}")
        print(f"View Team button: {view_team_button}")
        print(f"Exit button: {exit_button}")

        register_button.config(command=self.open_registration_window)
        login_button.config(command=self.open_login_window)
        view_team_button.config(command=self.view_team)
        exit_button.config(command=self.exit_program)
        
    def open_registration_window(self):
        """
        Open the registration window and bind its events.
        """
        registration_window, entries, register_button = self.view.create_registration_window()
        register_button.config(command=lambda: self.register_user(entries, registration_window))

    def register_user(self, entries, registration_window):
        """
        Handle user registration.

        Args:
            entries (dict): Dictionary containing user input data
            registration_window (tk.Toplevel): The registration window
        """
        username = entries['username'].get()
        password = entries['password'].get()
        first_name = entries['first_name'].get()
        last_name = entries['last_name'].get()
        dob = entries['date_of_birth'].get()
        position = entries['position'].get()

        # Check for empty fields
        if not all([username, password, first_name, last_name, dob, position]):
            self.view.show_error("Error", "All fields are required")
            return

        # Check that first and last names do not contain digits
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            self.view.show_error("Error", "First name and last name should not contain numbers")
            return

        # Register user
        if self.model.register_user(username, password, first_name, last_name, dob, position):
            self.view.show_message("Success", "User registered successfully")
            registration_window.destroy()
        else:
            self.view.show_error("Error", "Could not register user")

    def open_login_window(self):
        """
        Open the login window and bind its events.
        """
        login_window, username_entry, password_entry, login_button = self.view.create_login_window()
        login_button.config(command=lambda: self.login_user(username_entry.get(), password_entry.get(), login_window))

    def login_user(self, username, password, login_window):
        """
        Handle user login.

        Args:
            username (str): User's username
            password (str): User's password
            login_window (tk.Toplevel): The login window
        """
        user_id = self.model.verify_user(username, password)
        if user_id:
            self.view.show_message("Success", "Login successful")
            self.open_profile_window(user_id)
            login_window.destroy()
        else:
            self.view.show_error("Error", "Invalid username or password")

    def open_profile_window(self, user_id):
        """
        Open the user profile window and bind its events.

        Args:
            user_id (int): ID of the logged-in user
        """
        user_data = self.model.get_user_data(user_id)
        if not user_data:
            self.view.show_error("Error", "User not found")
            return

        profile_window, entries, save_button, delete_button = self.view.create_profile_window(user_data)
        



        save_button.config(command=lambda: self.save_profile_changes(user_id, entries, profile_window))
        delete_button.config(command=lambda: self.delete_account(user_id, profile_window))

    def save_profile_changes(self, user_id, entries, profile_window):
        """
        Handle saving of profile changes.

        Args:
            user_id (int): ID of the user
            entries (dict): Dictionary containing updated user data
            profile_window (tk.Toplevel): The profile window
        """
        update_data = []
        for key, entry in entries.items():
            value = entry.get()
            if key == 'email':
                if value and '@' not in value:
                    self.view.show_error("Error", "Email must contain @")
                    return
            elif key == 'jersey_number':
                if value and (not value.isdigit() or not (1 <= int(value) <= 99)):
                    self.view.show_error("Error", "Jersey number must be a number between 1 and 99")
                    return
            elif key in ['height']:
                if not value.isdigit() and value:
                    self.view.show_error("Error", f"{key.replace('_', ' ').title()} must be a number")
                    return
            elif key in ['primary_position', 'secondary_position']:
                if value and value not in ['ST', 'CF', 'RW', 'LW', 'CAM', 'CM', 'CDM', 'RM', 'LM', 'CB', 'RB', 'LB', 'GK']:
                    self.view.show_error("Error", f"{key.replace('_', ' ').title()} must be one of the specified positions")
                    return
            elif key == 'preferred_foot':
                if value and value not in ['Right', 'Left']:
                    self.view.show_error("Error", "Preferred Foot must be either 'Right' or 'Left'")
                    return
            update_data.append(value)

        if self.model.update_user_profile(user_id, update_data):
            self.view.show_message("Success", "Profile updated successfully")
            profile_window.destroy()
        else:
            self.view.show_error("Error", "Could not update profile")

    def delete_account(self, user_id, profile_window):
        """
        Handle account deletion.

        Args:
            user_id (int): ID of the user to delete
            profile_window (tk.Toplevel): The profile window
        """
        if self.view.ask_yes_no("Confirm Deletion", "Are you sure you want to delete this account?"):
            if self.model.delete_user(user_id):
                self.view.show_message("Success", "Account deleted successfully")
                profile_window.destroy()
            else:
                self.view.show_error("Error", "Could not delete account")

    def view_team(self):
        """
        Handle team view display.
        """
        team_data = self.model.get_team_data()
        self.view.create_team_view_window(team_data)

    def exit_program(self):
        """
        Handle program exit.
        """
        self.model.close_connection()
        self.view.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballTeamController(root)
    root.mainloop()