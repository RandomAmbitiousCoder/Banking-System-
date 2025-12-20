import customtkinter as ctk
from PIL import Image
import mysql.connector as ms
from CTkMessagebox import CTkMessagebox
import bcrypt


# =======================
# APP (ROOT CONTROLLER)
# =======================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x500")
        self.title("CTk Banking System")

        # ---- Database ----
        self.mydb = ms.connect(
            host="localhost",
            user="root",
            password="Innocent@2008"
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS BankingSystem")
        self.cursor.execute("USE BankingSystem")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            balance DECIMAL(10,2) DEFAULT 0.00
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            type VARCHAR(50),
            amount DECIMAL(10,2),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)


        # ---- Root screens ----
        self.screens = {
            "Login": Login,
            "SignUp": SignUp,
            "Menue": Menue
        }

        self.change_root("Login")

    def change_root(self, name):
        for widget in self.winfo_children():
            widget.destroy()

        self.screens[name](self)


# =======================
# LOGIN
# =======================

class Login(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app, fg_color="transparent")
        self.app = app

        self.show_img = ctk.CTkImage(Image.open("show.png"), size=(26, 26))
        self.hide_img = ctk.CTkImage(Image.open("hide.png"), size=(26, 26))

        ctk.CTkLabel(self, text='Login', font=('Rockwell', 50, 'bold')).grid(row=0, column=0, columnspan=2, pady=(100, 10), padx=20)

        self.login_email = ctk.CTkEntry(self, placeholder_text='Email', width=300, font=('Rockwell', 20))

        self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.login_password = ctk.CTkEntry(self.password_frame, placeholder_text='Password', show='*', width=300, font=('Rockwell', 20))
        self.show = ctk.CTkButton(self.password_frame, image=self.show_img, fg_color='transparent', hover=False, width=28, text='', command=lambda:self.toggle_password())

        self.login_button = ctk.CTkButton(
            self, text='Login', font=('Rockwell', 20, 'bold'),
            command=lambda: self.login()
        )
        self.sign_up = ctk.CTkButton(
            self, text='Sign Up?', font=('Rockwell', 20, 'bold'),
            cursor='hand2', hover_color='#242424', fg_color='transparent',
            command=lambda: self.app.change_root("SignUp")
        )
        self.sign_up.grid(row=4, column=1, columnspan=2, pady=(30, 10),  sticky='e')

        # --- layout with grid ---
        
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

        self.pack()

    def toggle_password(self):
        if self.login_password.cget("show") == "*":
            self.login_password.configure(show="")
            self.show.configure(image=self.hide_img)
        else:
            self.login_password.configure(show="*")
            self.show.configure(image=self.show_img)

    def login(self):
        username = self.login_email.get()
        password = self.login_password.get().encode()

        self.app.cursor.execute(
            "SELECT password FROM users WHERE username=%s",
            (username,)
        )
        user = self.app.cursor.fetchone()

        if user and bcrypt.checkpw(password, user[1].encode()):
            self.app.current_user = user[0]

            self.app.change_root("Menue")
        else:
            CTkMessagebox(
                title="Error",
                message="Invalid credentials",
                icon="cancel"
            )


# =======================
# SIGN UP
# =======================

class SignUp(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app, fg_color="transparent")
        self.app = app

        self.show_img = ctk.CTkImage(Image.open("show.png"), size=(26, 26))
        self.hide_img = ctk.CTkImage(Image.open("hide.png"), size=(26, 26))

        self.signup_label = ctk.CTkLabel(self, text='Sign Up', font=('Rockwell', 50, 'bold'))
        self.signup_email = ctk.CTkEntry(self, placeholder_text='Email', width=300, font=('Rockwell', 20))

        # Password frame for entry and eye button
        self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.signup_password = ctk.CTkEntry(self.password_frame, placeholder_text='Password', show='*', width=300, font=('Rockwell', 20))
        self.show = ctk.CTkButton(
            self.password_frame, image=self.show_img, fg_color='transparent', hover=False, width=28, text='',
            command=lambda: self.toggle_password()
        )

        self.signup_button = ctk.CTkButton(
            self, text='Sign Up', font=('Rockwell', 20, 'bold'),
            command=lambda: self.signup()
        )

        self.back = ctk.CTkButton(
            self, text='Back to Login', font=('Rockwell', 20, 'bold'),
            cursor='hand2', hover_color='#242424', fg_color='transparent',
            command=lambda: self.app.change_root("Login")
        )
        # --- layout with grid ---
        self.signup_label.grid(row=0, column=0, columnspan=2, pady=(100, 10), padx=20)
        self.signup_email.grid(row=1, column=0, columnspan=2, pady=(10, 10), padx=20, sticky ='ew')
        self.password_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=20, sticky='ew')
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=20)
        self.back.grid(row=4, column=1, columnspan=2, pady=(30, 10), sticky='e')

        # Place password entry and eye button inside password_frame
        self.signup_password.grid(row=0, column=0, sticky='ew')
        self.show.grid(row=0, column=1, padx=(5,0), sticky='w')
        self.password_frame.grid_columnconfigure(0, weight=1)

        # Bind Enter key to sign up
        self.signup_email.bind('<Return>', lambda event: self.signup())
        self.signup_password.bind('<Return>', lambda event: self.signup())

        self.pack()  # don’t change pack manager

    

    def toggle_password(self):
        if self.signup_password.cget("show") == "*":
            self.signup_password.configure(show="")
            self.show.configure(image=self.hide_img)
        else:
            self.signup_password.configure(show="*")
            self.show.configure(image=self.show_img)
    def signup(self):
        username = self.signup_email.get()
        password = self.signup_password.get().encode()

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            self.app.cursor.execute(
                "INSERT INTO users VALUES (%s, %s)",
                (username, hashed.decode())
            )
            self.app.mydb.commit()

            CTkMessagebox(
                title="Success",
                message="Account created",
                icon="check"
            )
            self.app.change_root("Login")

        except ms.Error:
            CTkMessagebox(
                title="Error",
                message="User already exists",
                icon="cancel"
            )


# =======================
# MENUE
# =======================
class Menue(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        # --- state ---
        self.extend = False
        self.button_positions = {
            "home": 130,
            "service": 200,
            "update": 270,
            "contact": 340,
            "about": 410
        }

        # --- images ---
        self.toggle_img = ctk.CTkImage(Image.open("toggle_btn_icon.png"), size=(28, 28))
        self.close_img = ctk.CTkImage(Image.open("close_btn_icon.png"), size=(28, 28))
        self.home_img = ctk.CTkImage(Image.open("home.png"), size=(28, 28))
        self.service_img = ctk.CTkImage(Image.open("services_icon.png"), size=(28, 28))
        self.update_img = ctk.CTkImage(Image.open("updates_icon.png"), size=(28, 28))
        self.contact_img = ctk.CTkImage(Image.open("contact_icon.png"), size=(28, 28))
        self.about_img = ctk.CTkImage(Image.open("about_icon.png"), size=(28, 28))

        # --- frames ---
        self.menuebar = ctk.CTkFrame(self, fg_color="#383838", width=51, corner_radius=0)
        self.menuebar.pack(side="left", fill="y")

        self.pageframe = ctk.CTkFrame(self)
        self.pageframe.pack(side="left", fill="both", expand=True)

        # --- indicator ---
        self.indicator = ctk.CTkLabel(
            self.menuebar,
            fg_color="white",
            text="",
            width=4,
            height=40
        )
        self.indicator.place(x=0, y=130)

        # --- toggle button ---
        self.toggle_btn = ctk.CTkButton(
            self.menuebar,
            image=self.toggle_img,
            text="",
            width=0,
            fg_color="#383838",
            hover_color="#303030",
            command=self.toggle_menu
        )
        self.toggle_btn.place(x=5, y=10)

        # --- menu buttons ---
        self.create_button("home", self.home_img, 130, Home)
        self.create_button("service", self.service_img, 200, Service)
        self.create_button("update", self.update_img, 270, Update)
        self.create_button("contact", self.contact_img, 340, Contact)
        self.create_button("about", self.about_img, 410, About)

        self.pack(fill="both", expand=True)
        self.load_page("home", Home)

    # ------------------
    # helpers
    # ------------------

    def create_button(self, name, image, y, page_class):
        btn = ctk.CTkButton(
            self.menuebar,
            image=image,
            text="",
            width=0,
            height=40,
            fg_color="#383838",
            hover_color="#303030",
            command=lambda: self.load_page(name, page_class)
        )
        btn.place(x=5, y=y)

    def load_page(self, name, page_class):
        self.indicator.place(y=self.button_positions[name])

        for w in self.pageframe.winfo_children():
            w.destroy()

        page_class(self.pageframe).pack(fill="both", expand=True)

        if self.extend:
            self.toggle_menu()

    def toggle_menu(self):
        if not self.extend:
            self.menuebar.configure(width=200)
            self.toggle_btn.configure(image=self.close_img)
            self.extend = True
        else:
            self.menuebar.configure(width=51)
            self.toggle_btn.configure(image=self.toggle_img)
            self.extend = False


# =======================
# VISUAL PAGES
# =======================

class Home(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        app = parent.master
        app.cursor.execute(
            "SELECT balance FROM users WHERE id=%s",
            (app.current_user,)
        )
        balance = app.cursor.fetchone()[0]


        ctk.CTkLabel(self, text="🏠 Home", font=("Rockwell", 40)).pack(pady=40)


class Service(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="⚙️ Services", font=("Rockwell", 40)).pack(pady=40)


class Update(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="🔔 Updates", font=("Rockwell", 40)).pack(pady=40)


class Contact(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="📞 Contact", font=("Rockwell", 40)).pack(pady=40)


class About(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="ℹ️ About", font=("Rockwell", 40)).pack(pady=40)


# =======================
# RUN APP
# =======================

app = App()
app.mainloop()
