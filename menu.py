from customtkinter import *
from tkinter import colorchooser, Canvas
from PIL import Image



class CtWindow(CTk):
    def __init__(self):
        super().__init__()

        img = CTkImage(
            light_image=Image.open("ping-pongphoto.png"),
            dark_image=Image.open("ping-pongphoto.png"),
            size=(100, 100)
        )
        self.host = None
        self.port = None

        self.title('Ping-Pong')
        self.geometry('300x500')

        CTkLabel(self, text='Connect to server:', font=('Comic Sans MS', 20, 'bold')).pack(pady=15, padx=20, anchor='w')

        self.label = CTkLabel(self, image=img, text="")
        self.label.pack(pady=20)

        self.host_entry = CTkEntry(self, placeholder_text='Введіть хост: ', height=50)
        self.host_entry.pack(padx=20, pady=15, anchor='w', fill='x')

        self.port_entry = CTkEntry(self, placeholder_text='Введіть порт сервера: ', height=50)
        self.port_entry.pack(padx=20, anchor='w', fill='x')

        CTkButton(self, text='Приєднатися', command=self.open_game, height=50).pack(pady=15, padx=20, fill='x')





    def open_game(self):
        self.host = self.host_entry.get()
        self.port = int(self.port_entry.get())
        self.destroy()

