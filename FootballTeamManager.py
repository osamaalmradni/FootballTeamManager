import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from tkcalendar import DateEntry
import mysql.connector
from PIL import Image, ImageTk
import io
from datetime import datetime
import bcrypt

class FootballTeamManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Football Team Manager")
        self.master.geometry("800x600")
        self.master.configure(bg='#ffffff')

        self.button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5}

        # Set up database connection
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="football_team"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Could not connect to database: {err}")
            self.master.quit()

        self.create_main_window()

    def create_main_window(self):
        # Main frame
        main_frame = tk.Frame(self.master, bg='#ffffff')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Football Team Manager", font=("Arial", 24, "bold"), bg='#ffffff', fg='#000000')
        title_label.pack(pady=20)

        # Buttons
        button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5}

        register_button = tk.Button(main_frame, text="Register", command=self.open_registration_window, **button_style)
        register_button.pack(pady=10)

        login_button = tk.Button(main_frame, text="Login", command=self.open_login_window, **button_style)
        login_button.pack(pady=10)

        view_team_button = tk.Button(main_frame, text="View Team", command=self.view_team, **button_style)
        view_team_button.pack(pady=10)

        exit_button = tk.Button(main_frame, text="Exit", command=self.exit_program, **button_style)
        exit_button.pack(pady=10)

    def open_registration_window(self):
        registration_window = tk.Toplevel(self.master)
        registration_window.title("Register")
        registration_window.geometry("600x700")
        registration_window.configure(bg='#ffffff')

        # Registration form
        form_frame = tk.Frame(registration_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        labels = ['Username', 'Password', 'First Name', 'Last Name', 'Date of Birth', 'Position']
        entries = {}

        for label in labels:
            tk.Label(form_frame, text=label, font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
            if label == 'Position':
                # Position dropdown with only predefined options
                entry = ttk.Combobox(form_frame, values=['Player', 'Coach'], font=("Arial", 12))
                entry.config(state='readonly')  # Make it readonly
            elif label == 'Date of Birth':
                # Date entry for date of birth
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='y-mm-dd')
            else:
                entry = tk.Entry(form_frame, font=("Arial", 12))
            entry.pack(fill='x', pady=5)
            entries[label.lower().replace(' ', '_')] = entry


        # Photo upload
        self.photo = None
        photo_button = tk.Button(form_frame, text="Upload Photo", command=lambda: self.upload_photo(form_frame), **self.button_style)
        photo_button.pack(pady=10)

        # Register button
        register_button = tk.Button(form_frame, text="Register", command=lambda: self.register_user(entries, registration_window), **self.button_style)
        register_button.pack(pady=20)

    def upload_photo(self, frame):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            photo = Image.open(file_path)
            photo.thumbnail((100, 100))
            self.original_photo = photo 
            photo_image = ImageTk.PhotoImage(photo)
            label = tk.Label(frame, image=photo_image)
            label.image = photo_image
            label.grid(row=len(frame.grid_slaves()), column=0, columnspan=2, pady=10)  
            self.photo_path = file_path  # Store the path of the uploaded photo

    def register_user(self, entries, registration_window):
        # Get values from entries
        username = entries['username'].get()
        password = entries['password'].get()
        first_name = entries['first_name'].get()
        last_name = entries['last_name'].get()
        dob = entries['date_of_birth'].get()
        position = entries['position'].get()

        # Validate inputs
        if not all([username, password, first_name, last_name, dob, position]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Convert photo to binary
            if hasattr(self, 'photo_path') and self.photo_path:
                with open(self.photo_path, 'rb') as file:
                    photo_binary = file.read()
            else:
                photo_binary = None

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Find the first available ID
            self.cursor.execute("SELECT id FROM users ORDER BY id")
            used_ids = set(id for (id,) in self.cursor.fetchall())

            first_available_id = 1
            while first_available_id in used_ids:
                first_available_id += 1

            # Insert into database
            query = """INSERT INTO users 
                    (id, username, password, first_name, last_name, date_of_birth, position, photo) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (first_available_id, username, hashed_password, first_name, last_name, dob, position, photo_binary))
            self.db.commit()
            messagebox.showinfo("Success", "User registered successfully")
            registration_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Could not register user: {err}")

    def open_login_window(self):
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.geometry("400x300")
        login_window.configure(bg='#ffffff')

        # Login form
        form_frame = tk.Frame(login_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(form_frame, text="Username", font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
        username_entry = tk.Entry(form_frame, font=("Arial", 12))
        username_entry.pack(fill='x', pady=5)

        tk.Label(form_frame, text="Password", font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
        password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*")
        password_entry.pack(fill='x', pady=5)

        login_button = tk.Button(form_frame, text="Login", command=lambda: self.login_user(username_entry.get(), password_entry.get(), login_window), **self.button_style)
        login_button.pack(pady=20)
        
    def login_user(self, username, password, login_window):
        try:
            query = "SELECT id, password FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                messagebox.showinfo("Success", "Login successful")
                self.open_profile_window(result[0])
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Could not verify user: {err}")

    def exit_program(self):
        self.db.close()
        self.master.quit()

    def open_profile_window(self, user_id):
        profile_window = tk.Toplevel(self.master)
        profile_window.title("User Profile")
        profile_window.geometry("600x800")
        profile_window.configure(bg='#ffffff')

        # Fetch user data
        query = """SELECT username, first_name, last_name, date_of_birth, position, 
                email, jersey_number, street, building_number, postal_code, city, 
                primary_position, secondary_position, height, preferred_foot, photo 
                FROM users WHERE id = %s"""
        self.cursor.execute(query, (user_id,))
        user_data = self.cursor.fetchone()

        if not user_data:
            messagebox.showerror("Error", "User not found")
            return

        # Create form
        form_frame = tk.Frame(profile_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        labels = ['Username', 'First Name', 'Last Name', 'Date of Birth', 'Position',
                'Email', 'Jersey Number', 'Street', 'Building Number', 'Postal Code',
                'City', 'Primary Position', 'Secondary Position', 'Height', 'Preferred Foot']
        
        entries = {}

        for i, label in enumerate(labels):
                tk.Label(form_frame, text=label, font=("Arial", 12), bg='#ffffff').grid(row=i, column=0, sticky='w', pady=5)
                if label == 'Date of Birth':
                    # Date entry for date of birth
                    entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='y-mm-dd') ### Updated for date picker
                else:
                    entry = tk.Entry(form_frame, font=("Arial", 12))
                entry.grid(row=i, column=1, sticky='ew', pady=5)
                entry.insert(0, str(user_data[i]) if user_data[i] else '')
                entries[label.lower().replace(' ', '_')] = entry
                
        # Display photo if available
        if user_data[-1]:
            photo = Image.open(io.BytesIO(user_data[-1]))
            photo.thumbnail((100, 100))
            self.original_photo = photo 
            photo_image = ImageTk.PhotoImage(photo)
            photo_label = tk.Label(form_frame, image=photo_image)
            photo_label.image = photo_image
            photo_label.grid(row=len(labels), column=0, columnspan=2, pady=10)
    
        upload_button = tk.Button(form_frame, text="Upload New Photo", command=lambda: self.upload_photo(form_frame), **self.button_style)  
        upload_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        # Save changes button
        save_button = tk.Button(form_frame, text="Save Changes", 
                                command=lambda: self.save_profile_changes(user_id, entries, profile_window),
                                **self.button_style)
        save_button.grid(row=len(labels)+2, column=0, columnspan=2, pady=20)

        # Delete account button
        delete_button = tk.Button(form_frame, text="Delete Account", 
                                command=lambda: self.delete_account(user_id, profile_window),
                                **self.button_style)
        delete_button.grid(row=len(labels)+3, column=0, columnspan=2, pady=20)

    def save_profile_changes(self, user_id, entries, profile_window):
        # Define the required fields.
        required_fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'position']
        
        # Prepare the data for update.
        update_data = [entries[key].get() for key in entries]

        # Check for required fields.
        missing_fields = [field for field in required_fields if not entries[field].get().strip()]
        if missing_fields:
            messagebox.showerror("Error", f"The following fields are required: {', '.join(missing_fields)}")
            return

        try:
            # Include the photo binary data if available
            if hasattr(self, 'original_photo'):
                bio = io.BytesIO()
                self.original_photo.save(bio, format="PNG")
                photo_binary = bio.getvalue()
            else:
                # If no new photo, retrieve the existing photo from the database
                query = "SELECT photo FROM users WHERE id = %s"
                self.cursor.execute(query, (user_id,))
                photo_binary = self.cursor.fetchone()[0]

            # Update query
            query = """UPDATE users SET username=%s, first_name=%s, last_name=%s, date_of_birth=%s, 
                    position=%s, email=%s, jersey_number=%s, street=%s, building_number=%s, 
                    postal_code=%s, city=%s, primary_position=%s, secondary_position=%s, 
                    height=%s, preferred_foot=%s, photo=%s WHERE id=%s"""
            
            update_data.append(photo_binary)  # Include the photo binary in the update data
            update_data.append(user_id)  # Add user ID at the end of update data

            self.cursor.execute(query, tuple(update_data))
            self.db.commit()
            messagebox.showinfo("Success", "Profile updated successfully")
            profile_window.destroy()
        except mysql.connector.Error as err:
            if err.errno == 2013:
                messagebox.showerror("Error", "Lost connection to MySQL server during query. Please try again.")
            else:
                messagebox.showerror("Error", f"Could not update profile: {err}")

    def delete_account(self, user_id, profile_window):
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this account?"):
            # Delete query
            query = "DELETE FROM users WHERE id = %s"

            try:
                self.cursor.execute(query, (user_id,))
                self.db.commit()
                messagebox.showinfo("Success", "Account deleted successfully")
                profile_window.destroy()  # Close the profile window
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Could not delete account: {err}")

    def view_team(self):
        team_window = tk.Toplevel(self.master)
        team_window.title("Team View")
        team_window.geometry("1000x600") 
        team_window.configure(bg='#ffffff')

        # Create a frame for the team view
        team_frame = tk.Frame(team_window, bg='#ffffff')
        team_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Create a treeview widget
        columns = ('', 'First Name', 'Last Name', 'Date of Birth', 'Position', 'Email', 'Jersey Number', 
                'Street', 'Building Number', 'Postal Code', 'City', 'Primary Position', 'Secondary Position', 
                'Height', 'Preferred Foot')
        tree = ttk.Treeview(team_frame, columns=columns, show='headings')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, stretch=True)  # Set initial width, can be adjusted

        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(team_frame, orient='horizontal', command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side='bottom', fill='x')

        tree.pack(expand=True, fill='both')

        # Fetch team data
        query = """SELECT first_name, last_name, date_of_birth, position, email, jersey_number, 
                        street, building_number, postal_code, city, primary_position, secondary_position, 
                        height, preferred_foot 
                FROM users 
                ORDER BY CASE WHEN position='Coach' THEN 0 ELSE 1 END, last_name"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Insert data into treeview with numbering and separator row
        coach_counter = 1
        player_counter = 1
        coaches_inserted = False  # Flag to track if 'Coaches' header has been inserted
        for row in data:
            if row[3] == 'Coach':
                if not coaches_inserted:
                    # Insert separator row for coaches if not already inserted
                    tree.insert('', 'end', values=('', 'Coaches', '', '', '', '', '', '', '', '', '', '', '', '', ''), tags=('separator',))
                    coaches_inserted = True
                tree.insert('', 'end', values=(coach_counter, *row))
                coach_counter += 1
            else:
                if player_counter == 1:
                    # Insert separator row
                    tree.insert('', 'end', values=('', 'Players', '', '', '', '', '', '', '', '', '', '', '', '', ''), tags=('separator',))
                tree.insert('', 'end', values=(player_counter, *row))
                player_counter += 1

        # Adjust column widths based on content
        font_measure = font.Font()
        for col in columns:
            tree.column(col, width=font_measure.measure(col) + 10)  # Initial width based on header
            for item in tree.get_children():
                item_text = tree.item(item, 'values')[columns.index(col)]
                tree.column(col, width=max(tree.column(col, 'width'), font_measure.measure(item_text) + 10))

        # Apply styles
        tree.tag_configure('separator', background='#e0e0e0', font=('Arial', 12, 'bold'))

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballTeamManager(root)
    root.mainloop()