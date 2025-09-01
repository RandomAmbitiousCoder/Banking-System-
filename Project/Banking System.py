import customtkinter as ctk
from PIL import Image
import mysql.connector as ms
from CTkMessagebox import CTkMessagebox
import bcrypt


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk Banking System")

        # --- DB setup ---
        self.mydb = ms.connect(
            host='localhost',
            user='root',
            password='Innocent@2008'
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS BankingSystem")
        self.cursor.execute("USE BankingSystem")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        self.button_positions = {
            'home': 130,
            'service': 200,
            'update': 270,
            'contact': 340,
            'about': 410
        }

        self.extend = False

        # --- Images ---
        self.show = ctk.CTkImage(Image.open("show.png"), size=(28, 28))
        self.hide = ctk.CTkImage(Image.open("hide.png"), size=(28, 28))
        self.toggle = ctk.CTkImage(Image.open("toggle_btn_icon.png"), size=(28, 28))
        self.home = ctk.CTkImage(Image.open("home.png"), size=(28, 28))
        self.service = ctk.CTkImage(Image.open("services_icon.png"), size=(28, 28))
        self.updated = ctk.CTkImage(Image.open("updates_icon.png"), size=(28, 28))
        self.contact = ctk.CTkImage(Image.open("contact_icon.png"), size=(28, 28))
        self.about_icon = ctk.CTkImage(Image.open("about_icon.png"), size=(28, 28))
        self.close = ctk.CTkImage(Image.open("close_btn_icon.png"), size=(28, 28))

        # --- Shared Frames ---
        self.pageframe = ctk.CTkFrame(self)
        self.menuebar = ctk.CTkFrame(self, fg_color='#383838', corner_radius=0)

        # --- Menu Bar Buttons ---
        self.indicator = self.Indicator(self)
        self.toggle_menue_button = ctk.CTkButton(
            self.menuebar, image=self.toggle, fg_color='#383838',
            hover_color='#303030', width=0, text='',
            command=lambda: self.extend_menue()
        )
        self.toggle_menue_button.place(x=4.5, y=10)

        self.homebtn = ctk.CTkButton(
            self.menuebar, image=self.home, fg_color='#383838',
            hover_color='#303030', width=0, text='', height=40,
            command=lambda: self.indicator.switch_position('home')
        )
        self.homelabel = ctk.CTkLabel(self.menuebar, text='Home', font=('Rockwell', 20, 'bold'))

        self.servicebtn = ctk.CTkButton(
            self.menuebar, image=self.service, fg_color='#383838',
            hover_color='#303030', width=0, text='', height=40,
            command=lambda: self.indicator.switch_position('service')
        )
        self.servicelabel = ctk.CTkLabel(self.menuebar, text='Service', font=('Rockwell', 20, 'bold'))

        self.contactbtn = ctk.CTkButton(
            self.menuebar, image=self.contact, fg_color='#383838',
            hover_color='#303030', width=0, text='', height=40,
            command=lambda: self.indicator.switch_position('contact')
        )
        self.contactlabel = ctk.CTkLabel(self.menuebar, text='Contact', font=('Rockwell', 20, 'bold'))

        self.updatebtn = ctk.CTkButton(
            self.menuebar, image=self.updated, fg_color='#383838',
            hover_color='#303030', width=0, text='', height=40,
            command=lambda: self.indicator.switch_position('update')
        )
        self.updatelabel = ctk.CTkLabel(self.menuebar, text='Update', font=('Rockwell', 20, 'bold'))

        self.aboutbtn = ctk.CTkButton(
            self.menuebar, image=self.about_icon, fg_color='#383838',
            hover_color='#303030', width=0, text='', height=40,
            command=lambda: self.indicator.switch_position('about')
        )
        self.aboutlabel = ctk.CTkLabel(self.menuebar, text='About', font=('Rockwell', 20, 'bold'))

        # --- First screen = Login ---
        self.current_screen = None
        self.screen_change(self.Login)

    # --- Screen Manager ---
    def screen_change(self, screen):
        if self.current_screen:
            self.current_screen.pack_forget()
            self.current_screen.destroy()
        self.current_screen = screen(self)
        return self.current_screen
    

    # --- Pages ---
    class Login(ctk.CTkFrame):
        def __init__(self, app):
            super().__init__(app, fg_color="transparent")
            self.app = app

            self.login_label = ctk.CTkLabel(self, text='Login', font=('Rockwell', 50, 'bold'))
            self.login_email = ctk.CTkEntry(self, placeholder_text='Email', width=300, font=('Rockwell', 20))

            # Create a frame for password entry and eye button
            self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.login_password = ctk.CTkEntry(self.password_frame, placeholder_text='Password', show='*', width=300, font=('Rockwell', 20))
            self.show = ctk.CTkButton(self.password_frame, image=self.app.show, fg_color='transparent', hover=False, width=28, text='', command=lambda:self.app.toggle_password())

            self.login_button = ctk.CTkButton(
                self, text='Login', font=('Rockwell', 20, 'bold'),
                command=lambda: self.login()
            )
            self.sign_up = ctk.CTkButton(
                self, text='Sign Up?', font=('Rockwell', 20, 'bold'),
                cursor='hand2', hover_color='#242424', fg_color='transparent',
                command=lambda: self.app.screen_change(self.app.SignUp)
            )

            # --- layout with grid ---
            self.login_label.grid(row=0, column=0, columnspan=2, pady=(100, 10), padx=20)
            self.login_email.grid(row=1, column=0, columnspan=2, pady=(10, 10), padx=20, sticky='ew')
            self.password_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=20, sticky='ew')
            self.login_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=20)

            # Place password entry and eye button inside password_frame
            self.login_password.grid(row=0, column=0, sticky='ew')
            self.show.grid(row=0, column=1, padx=(5,0), sticky='w')
            self.password_frame.grid_columnconfigure(0, weight=1)

            # Bind Enter key to login
            self.login_email.bind('<Return>', lambda event: self.login())
            self.login_password.bind('<Return>', lambda event: self.login())

            self.pack()  # don’t change pack manager

        def login(self):
            username = self.login_email.get()
            password = self.login_password.get().encode('utf-8')

            if username and password:
                self.app.cursor.execute(
                    "SELECT password FROM users WHERE username=%s",
                    (username,)
                )
                user = self.app.cursor.fetchone()
                if user:
                    stored_hash = user[0].encode('utf-8')
                    if bcrypt.checkpw(password, stored_hash):
                        self.app.screen_change(self.app.Menue)
                    else:
                        CTkMessagebox(title="Error", message="Invalid username or password", icon='cancel').get()
                        self.sign_up.grid(row=4, column=1, pady=20, sticky='e', padx=(0, 20))
                        
                else:
                    CTkMessagebox(title="Error", message="Username not Found", icon='cancel').get()
                    self.sign_up.grid(row=4, column=1, pady=20, sticky='e', padx=(0, 20))

            else:
                CTkMessagebox(title="Error", message="Please fill in all fields", icon='retry')

    class SignUp(ctk.CTkFrame):
        def __init__(self, app):
            super().__init__(app, fg_color="transparent")
            self.app = app

            self.signup_label = ctk.CTkLabel(self, text='Sign Up', font=('Rockwell', 50, 'bold'))
            self.signup_email = ctk.CTkEntry(self, placeholder_text='Email', width=300, font=('Rockwell', 20))

            # Password frame for entry and eye button
            self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.signup_password = ctk.CTkEntry(self.password_frame, placeholder_text='Password', show='*', width=300, font=('Rockwell', 20))
            self.show = ctk.CTkButton(
                self.password_frame, image=self.app.show, fg_color='transparent', hover=False, width=28, text='',
                command=lambda: self.app.toggle_password()
            )

            self.signup_button = ctk.CTkButton(
                self, text='Sign Up', font=('Rockwell', 20, 'bold'),
                command=lambda: self.sign_up()
            )

            # --- layout with grid ---
            self.signup_label.grid(row=0, column=0, columnspan=2, pady=(100, 10), padx=20)
            self.signup_email.grid(row=1, column=0, columnspan=2, pady=(10, 10), padx=20, sticky ='ew')
            self.password_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=20, sticky='ew')
            self.signup_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=20)

            # Place password entry and eye button inside password_frame
            self.signup_password.grid(row=0, column=0, sticky='ew')
            self.show.grid(row=0, column=1, padx=(5,0), sticky='w')
            self.password_frame.grid_columnconfigure(0, weight=1)

            # Bind Enter key to sign up
            self.signup_email.bind('<Return>', lambda event: self.sign_up())
            self.signup_password.bind('<Return>', lambda event: self.sign_up())

            self.pack()  # don’t change pack manager

        def sign_up(self):
            username = self.signup_email.get()
            password = self.signup_password.get().encode('utf-8')
            if username and password:
                try:
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                    self.app.cursor.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)",
                        (username, hashed.decode('utf-8'))
                    )
                    self.app.mydb.commit()
                    CTkMessagebox(title="Success", message="User created successfully", icon='check')
                    self.app.screen_change(self.app.Login)
                except ms.Error as e:
                    CTkMessagebox(title="Error", message=f"Error creating user: {e}", icon='cancel')
            else:
                CTkMessagebox(title="Error", message="Please fill in all fields", icon='retry')

    class Menue(ctk.CTkFrame):
        def __init__(self, app):
            super().__init__(app, fg_color="transparent")
            self.app = app

            
            self.app.menuebar.pack(side='left', fill='both')
            self.app.menuebar.propagate(False)
            self.app.menuebar.configure(width=51)

            self.app.homebtn.place(x=4.5, y=130)
            self.app.homelabel.place(x=60, y=137)

            self.app.servicebtn.place(x=4.5, y=200)
            self.app.servicelabel.place(x=60, y=207)

            self.app.updatebtn.place(x=4.5, y=270)
            self.app.updatelabel.place(x=60, y=277)

            self.app.contactbtn.place(x=4.5, y=340)
            self.app.contactlabel.place(x=60, y=347)

            self.app.aboutbtn.place(x=4.5, y=410)
            self.app.aboutlabel.place(x=60, y=417)

            self.pack()  # keep pack manager

    # --- Menu Extender ---
    def extend_menue(self):
        if not self.extend:
            self.menuebar.configure(width=200)
            self.toggle_menue_button.configure(image=self.close)
            self.extend = True
        else:
            self.menuebar.configure(width=51)
            self.toggle_menue_button.configure(image=self.toggle)
            self.extend = False

    # --- Indicator ---
    class Indicator:
        def __init__(self, app, x=0, y=130):
            self.app = app
            self.x = x
            self.y = y
            self.indicator = ctk.CTkLabel(
                self.app.menuebar, fg_color='white', text='',
                height=40, width=3.5
            )
            self.indicator.place(x=self.x, y=self.y)

        def switch_position(self, button_name, x=0):
            self.x = x
            self.y = self.app.button_positions[button_name]
            self.indicator.place(x=self.x, y=self.y)

            if self.app.extend:
                self.app.extend_menie()

    def toggle_password(self):
        frame = self.current_screen
        # Use login_password if it exists, else use signup_password
        entry = getattr(frame, "login_password", None) or getattr(frame, "signup_password", None)
        btn = getattr(frame, "show", None)
        if entry and btn:
            if entry.cget('show') == '*':
                entry.configure(show='')
                btn.configure(image=self.hide)
            else:
                entry.configure(show='*')
                btn.configure(image=self.show)


if __name__ == "__main__":
    app = App()
    app.mainloop()
