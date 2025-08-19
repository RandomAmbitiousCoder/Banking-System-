import customtkinter as ctk
from PIL import Image
import mysql.connector as ms


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

        #Icon Declaration
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
        self.pageframe = ctk.CTkFrame(self)
        self.pageframe.place(relwidth=1, relheight=1, x = 55)
        self.menuebar = ctk.CTkFrame(self, fg_color=  '#383838', corner_radius=0)
        self.menuebar.pack(side = 'left', fill ='both')
        self.menuebar.propagate(False)
        self.menuebar.configure(width = 51)


        #Icons
        self.indicator = self.Indicator(self)

        self.toggle_menue_button = ctk.CTkButton(self.menuebar, image = self.toggle,fg_color='#383838',hover_color='#303030',width = 0,text = '', command= lambda: self.extend_menue())
        self.toggle_menue_button.place(x =4.5 , y = 10)

        #Screen
        self.home_screen = self.Home(self)




        self.homebtn = ctk.CTkButton(self.menuebar, image=self.home, fg_color='#383838',hover_color='#303030', width=0, text='', height=40,command= lambda: self.indicator.switch_position('home'))
        self.homebtn.place(x = 4.5, y = 130)

        self.homelabel = ctk.CTkLabel(self.menuebar, text='Home', font=('Rockwell', 20 , 'bold'))
        self.homelabel.place(x= 60, y = 137)
        self.homelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('home'))



        self.servicebtn = ctk.CTkButton(self.menuebar, image=self.service, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda:self.indicator.switch_position('service'))
        self.servicebtn.place(x = 4.5, y =200 )

        self.servicelabel = ctk.CTkLabel(self.menuebar, text='service', font=('Rockwell', 20, 'bold'))
        self.servicelabel.place(x=60, y=207)
        self.servicelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('service'))




        self.updatebtn = ctk.CTkButton(self.menuebar, image=self.updated, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('update'))
        self.updatebtn.place(x = 4.5, y = 270)

        self.updatelabel = ctk.CTkLabel(self.menuebar, text='update', font=('Rockwell', 20, 'bold'))
        self.updatelabel.place(x=60, y=277)
        self.updatelabel.bind('<Button-1>', lambda e: self.indicator.switch_position('update'))


        self.contactbtn = ctk.CTkButton(self.menuebar, image=self.contact, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('contact'))
        self.contactbtn.place(x = 4.5, y = 340)

        self.contactlabel = ctk.CTkLabel(self.menuebar, text='contact', font=('Rockwell', 20, 'bold'))
        self.contactlabel.place(x=60, y=347)
        self.contactlabel.bind('<Button-1>', lambda e: self.indicator.switch_position('contact'))


        self.about = ctk.CTkButton(self.menuebar, image = self.about, fg_color='#383838',hover_color='#303030', width=0, text='',height=40, command= lambda: self.indicator.switch_position('about'))
        self.about.place(x = 4.5, y = 410)

        self.aboutlabel = ctk.CTkLabel(self.menuebar, text='about', font=('Rockwell', 20, 'bold'))
        self.aboutlabel.place(x=60, y=417)
        self.aboutlabel.bind('<Button-1>', lambda e: self.indicator.switch_position('about'))






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

