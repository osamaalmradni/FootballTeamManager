# view.py

import tkinter as tk
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry


class FootballTeamView:

    """
    The View component of the Football Team Manager application.
    Handles all GUI-related operations and user interactions.
    """
    def __init__(self, master):
        """
        Initialize the view.

        Args:
            master: The root window of the application
        """
        self.master = master
        self.master.title("Football Team Manager")
        self.master.geometry("800x600")
        self.master.configure(bg='#ffffff')

        self.button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5}

    def create_main_window(self):
        """
        Create the main window of the application.
        """
        main_frame = tk.Frame(self.master, bg='#ffffff')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        title_label = tk.Label(main_frame, text="Football Team Manager", font=("Arial", 24, "bold"), bg='#ffffff', fg='#000000')
        title_label.pack(pady=20)

        register_button = tk.Button(main_frame, text="Register", **self.button_style)
        register_button.pack(pady=10)

        login_button = tk.Button(main_frame, text="Login", **self.button_style)
        login_button.pack(pady=10)

        view_team_button = tk.Button(main_frame, text="View Team", **self.button_style)
        view_team_button.pack(pady=10)

        exit_button = tk.Button(main_frame, text="Exit", **self.button_style)
        exit_button.pack(pady=10)

        

        return register_button, login_button, view_team_button, exit_button

    def create_registration_window(self):
        """
        Create the registration window.

        Returns:
            tuple: Registration window and dictionary of entry fields
        """
        registration_window = tk.Toplevel(self.master)
        registration_window.title("Register")
        registration_window.geometry("600x700")
        registration_window.configure(bg='#ffffff')

        form_frame = tk.Frame(registration_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        labels = ['Username', 'Password', 'First Name', 'Last Name', 'Date of Birth', 'Position']
        entries = {}

        for label in labels:
            tk.Label(form_frame, text=label, font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
            
            if label == 'Position':
                entry = ttk.Combobox(form_frame, values=['Player', 'Coach'], font=("Arial", 12))
                entry.config(state='readonly')
            elif label == 'Password':
                entry = tk.Entry(form_frame, font=("Arial", 12), show='*')
            elif label == 'Date of Birth':
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='y-mm-dd')
            else:
                entry = tk.Entry(form_frame, font=("Arial", 12))
            entry.pack(fill='x', pady=5)
            entries[label.lower().replace(' ', '_')] = entry


        register_button = tk.Button(form_frame, text="Register", **self.button_style)
        register_button.pack(pady=20)

        return registration_window, entries, register_button

    def create_login_window(self):
        """
        Create the login window.

        Returns:
            tuple: Login window and entry fields for username and password
        """
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.geometry("400x300")
        login_window.configure(bg='#ffffff')

        form_frame = tk.Frame(login_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(form_frame, text="Username", font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
        username_entry = tk.Entry(form_frame, font=("Arial", 12))
        username_entry.pack(fill='x', pady=5)

        tk.Label(form_frame, text="Password", font=("Arial", 12), bg='#ffffff').pack(anchor='w', pady=5)
        password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*")
        password_entry.pack(fill='x', pady=5)

        login_button = tk.Button(form_frame, text="Login", **self.button_style)
        login_button.pack(pady=20)

        return login_window, username_entry, password_entry, login_button

    def create_profile_window(self, user_data):
        """
        Create the user profile window.

        Args:
            user_data (tuple): User data to populate the fields

        Returns:
            tuple: Profile window, dictionary of entry fields, and buttons
        """
        profile_window = tk.Toplevel(self.master)
        profile_window.title("User Profile")
        profile_window.geometry("600x800")
        profile_window.configure(bg='#ffffff')

        form_frame = tk.Frame(profile_window, bg='#ffffff')
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        labels = ['Username', 'First Name', 'Last Name', 'Date of Birth', 'Position',
                'Email', 'Street', 'Building Number', 'Postal Code',
                'City','Jersey Number', 'Primary Position', 'Secondary Position', 'Height', 'Preferred Foot']
        
        entries = {}
        positions = ['ST', 'CF', 'RW', 'LW', 'CAM', 'CM', 'CDM', 'RM', 'LM', 'CB', 'RB', 'LB', 'GK']
        preferred_foot = ['Right', 'Left']

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=("Arial", 12), bg='#ffffff').grid(row=i, column=0, sticky='w', pady=5)
            if label == 'Date of Birth':
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='y-mm-dd')
                entry.set_date(user_data[i] if user_data[i] else '2000-01-01')
                entry.grid(row=i, column=1, sticky='ew', pady=5)
            elif label == 'Primary Position' or label == 'Secondary Position':
                entry = tk.StringVar(value=user_data[i])
                tk.OptionMenu(form_frame, entry, *positions).grid(row=i, column=1, sticky='ew', pady=5)
            elif label == 'Preferred Foot':
                entry = tk.StringVar(value=user_data[i])
                tk.OptionMenu(form_frame, entry, *preferred_foot).grid(row=i, column=1, sticky='ew', pady=5)
            else:
                entry = tk.Entry(form_frame, font=("Arial", 12))
                entry.grid(row=i, column=1, sticky='ew', pady=5)
                entry.insert(0, str(user_data[i]) if user_data[i] else '')
            entries[label.lower().replace(' ', '_')] = entry

        save_button = tk.Button(form_frame, text="Save Changes", **self.button_style)
        save_button.grid(row=len(labels)+2, column=0, columnspan=2, pady=20)

        delete_button = tk.Button(form_frame, text="Delete Account", **self.button_style)
        delete_button.grid(row=len(labels)+3, column=0, columnspan=2, pady=20)

        return profile_window, entries, save_button, delete_button

    def create_team_view_window(self, team_data):
        """
        Create the team view window.

        Args:
            team_data (list): List of tuples containing team member data

        Returns:
            tk.Toplevel: Team view window
        """
        team_window = tk.Toplevel(self.master)
        team_window.title("Team View")
        team_window.geometry("1000x600")
        team_window.configure(bg='#ffffff')

        team_frame = tk.Frame(team_window, bg='#ffffff')
        team_frame.pack(expand=True, fill='both', padx=20, pady=20)

        columns = ('', 'First Name', 'Last Name', 'Date of Birth', 'Position', 'Email', 
                'Street', 'Building Number', 'Postal Code', 'City', 'Jersey Number', 'Primary Position', 'Secondary Position', 
                'Height', 'Preferred Foot')
        tree = ttk.Treeview(team_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, stretch=True)

        h_scrollbar = ttk.Scrollbar(team_frame, orient='horizontal', command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side='bottom', fill='x')

        tree.pack(expand=True, fill='both')

        coach_counter = 1
        player_counter = 1
        coaches_inserted = False
        for row in team_data:
            if row[3] == 'Coach':
                if not coaches_inserted:
                    tree.insert('', 'end', values=('', 'Coaches', '', '', '', '', '', '', '','', '', '', '', '', ''), tags=('separator',))
                    coaches_inserted = True
                tree.insert('', 'end', values=(coach_counter, *row))
                coach_counter += 1
            else:
                if player_counter == 1:
                    tree.insert('', 'end', values=('', 'Players', '', '', '', '', '', '', '', '', '', '', '', '', ''), tags=('separator',))
                tree.insert('', 'end', values=(player_counter, *row))
                player_counter += 1

        font_measure = font.Font()
        for col in columns:
            tree.column(col, width=font_measure.measure(col) + 10) 
            for item in tree.get_children():
                item_text = tree.item(item, 'values')[columns.index(col)]
                tree.column(col, width=max(tree.column(col, 'width'), font_measure.measure(item_text) + 10))


        tree.tag_configure('separator', background='#e0e0e0', font=('Arial', 12, 'bold'))

        return team_window

    def show_message(self, title, message):
        """
        Display a message box to the user.

        Args:
            title (str): Title of the message box
            message (str): Message to display
        """
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """
        Display an error message to the user.

        Args:
            title (str): Title of the error box
            message (str): Error message to display
        """
        messagebox.showerror(title, message)

    def ask_yes_no(self, title, message):
        """
        Ask the user a yes/no question.

        Args:
            title (str): Title of the question box
            message (str): Question to ask

        Returns:
            bool: True if user selects 'Yes', False otherwise
        """
        return messagebox.askyesno(title, message)



