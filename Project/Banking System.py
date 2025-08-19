import customtkinter as ctk
from PIL import Image
import mysql.connector as ms
from CTkMessagebox import CTkMessagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")

        self.button_positions = {
            'home': 130,
            'service': 200,
            'update': 270,
            'contact': 340,
            'about': 410
        }
        mydb = ms.connect(
            host = 'localhost',
            user = 'root',
            password = 'Innocent@2008'
        )
        self.cursor = mydb.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS BankingSystem")
        self.cursor.execute("USE BankingSystem")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(255),
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        mydb.commit()
        mydb.close()            

        self.extend = False


        #Image Declaration
        self.toggle = ctk.CTkImage(light_image=Image.open("toggle_btn_icon.png"),
                                                         dark_image=Image.open("toggle_btn_icon.png"),
                                                          size = (28,28))
        self.home  = ctk.CTkImage(light_image=Image.open("home.png"),
                                                          dark_image=Image.open("home.png"),
                                                          size = (28,28))
        self. service= ctk.CTkImage(light_image= Image.open('services_icon.png'),dark_image=Image.open('services_icon.png'), size = (28,28))
        self.updated = ctk.CTkImage(light_image = Image.open('updates_icon.png'),dark_image = Image.open('updates_icon.png'), size = (28,28))
        self.contact = ctk.CTkImage(light_image= Image.open('contact_icon.png'),dark_image = Image.open('contact_icon.png'), size = (28,28))
        self.about = ctk.CTkImage(light_image = Image.open('about_icon.png'),dark_image = Image.open('about_icon.png'), size = (28,28))
        self.close = ctk.CTkImage(light_image = Image.open('close_btn_icon.png'), dark_image=Image.open('close_btn_icon.png'), size = (28,28))


        #Frame


        #Icons
        self.pageframe = ctk.CTkFrame(self)
        
        self.menuebar = ctk.CTkFrame(self, fg_color=  '#383838', corner_radius=0)
        
        self.indicator = self.Indicator(self)
        self.toggle_menue_button = ctk.CTkButton(self.menuebar, image = self.toggle,fg_color='#383838',hover_color='#303030',width = 0,text = '', command= lambda: self.extend_menue())
        self.toggle_menue_button.place(x =4.5 , y = 10)
        
        self.homebtn = ctk.CTkButton(self.menuebar, image=self.home, fg_color='#383838',hover_color='#303030', width=0, text='', height=40,command= lambda: self.indicator.switch_position('home'))
        self.homelabel = ctk.CTkLabel(self.menuebar, text='Home', font=('Rockwell', 20 , 'bold'))
        
        self.servicebtn = ctk.CTkButton(self.menuebar, image=self.service, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda:self.indicator.switch_position('service'))
        self.servicelabel = ctk.CTkLabel(self.menuebar, text='service', font=('Rockwell', 20, 'bold'))
        
        self.contactbtn = ctk.CTkButton(self.menuebar, image=self.contact, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('contact'))
        self.contactlabel = ctk.CTkLabel(self.menuebar, text='contact', font=('Rockwell', 20, 'bold'))
        
        self.updatebtn = ctk.CTkButton(self.menuebar, image=self.updated, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('update'))
        self.updatelabel = ctk.CTkLabel(self.menuebar, text='update', font=('Rockwell', 20, 'bold'))

        self.about = ctk.CTkButton(self.menuebar, image = self.about, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('about'))
        self.aboutlabel = ctk.CTkLabel(self.menuebar, text='about', font=('Rockwell', 20, 'bold'))

        #Screen
        self.login_screen = self.Login(self)
        




        



    class Login:
        def __init__(self,app):
            self.app = app
            self.login_frame = ctk.CTkFrame(self.app, fg_color='transparent')
            self.login_label = ctk.CTkLabel(self.login_frame, text='Login', font=('Rockwell', 50, 'bold'))
            self.login_username = ctk.CTkEntry(self.login_frame, placeholder_text='Username', width=300, font=('Rockwell', 20))
            self.login_password = ctk.CTkEntry(self.login_frame, placeholder_text='Password', show='*', width=300, font=('Rockwell', 20))
            self.login_button = ctk.CTkButton(self.login_frame, text='Login', font=('Rockwell', 20,'bold'),command=lambda:self.login)

            self.login_frame.pack()
            self.login_label.pack(pady=10)
            self.login_username.pack(pady=20)
            self.login_password.pack(pady=(0,20))
            self.login_button.pack(pady=20)
        def login(self):
            self.login_username_value = self.login_username.cget()
            self.login_password_value = self.login_password.cget()
            if self.login_username_value and self.login_password_value:
                self.app.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (self.login_username_value, self.login_password_value))
                user = self.app.cursor.fetchone()
                if user:
                    self.login_frame.pack_forget()
                    self.app.pageframe.pack(fill='both', expand=True)
                    
                else:
                    ctk.CTkMessageBox(title="Error", message="Invalid username or password")
            else:
                ctk.CTkMessageBox(title="Error", message="Please fill in all fields")
            
        
    
    class Menue:
        def __init__(self,app):

            self.app.pageframe.place(relwidth=1, relheight=1, x = 55)
            self.app.menuebar.pack(side = 'left', fill ='both')
            self.app.menuebar.propagate(False)
            self.app.menuebar.configure(width = 51)

            self.app = app
            self.app.homebtn.place(x = 4.5, y = 130)

            self.app.homelabel.place(x= 60, y = 137)
            self.app.homelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('home'))



            self.app.servicebtn.place(x = 4.5, y =200 )

            self.app.servicelabel.place(x=60, y=207)
            self.app.servicelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('service'))




            self.app.updatebtn.place(x = 4.5, y = 270)

            self.app.updatelabel.place(x=60, y=277)
            self.app.updatelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('update'))


            self.app.contactbtn.place(x = 4.5, y = 340)

            self.app.contactlabel.place(x=60, y=347)
            self.app.contactlabel.bind('<Button-1>', lambda e: self.indicator.switch_position('contact'))


            self.app.about.place(x = 4.5, y = 410)

            self.app.aboutlabel.place(x=60, y=417)
            self.app.aboutlabel.bind('<Button-1>', lambda e: self.indicator.switch_position('about'))



    def extend_menue(self):

        if not self.extend :
            self.menuebar.configure(width= 200)
            self.toggle_menue_button.configure(image= self.close)
            self.extend = True
        elif self.extend:
            self.menuebar.configure(width= 51)
            self.toggle_menue_button.configure(image= self.toggle)
            self.extend = False







    class Indicator:
        def __init__(self, app ,x=0,y=130):
            self.app = app
            self.x = x
            self.y = y
            self.indicator = ctk.CTkLabel(self.app.menuebar, fg_color = 'white', text='', height= 40, width = 3.5)
            self.indicator.place(x = self.x, y = self.y)

        def switch_position(self, button_name, x= 0):
            self.x = x
            self.y = self.app.button_positions[button_name]
            self.indicator.place(x = self.x, y = self.y)

            if self.app.extend:
                self.app.extend_menue()

    class Home:
        def __init__(self, app):
            self.app = app
            self.profile = ctk.CTkButton(self.app.pageframe, text='',width = 45)
            self.profile.configure(height = self.profile.cget('width'), corner_radius= self.profile.cget('width')//2)
            self.profile.place(x=2, y=5, anchor='nw')
            








app = App()
app.mainloop()

