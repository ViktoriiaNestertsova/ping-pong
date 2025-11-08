from customtkinter import *
from tkinter import colorchooser, Canvas


class CtWindow(CTk):
    def __init__(self):
        super().__init__()

        self.host = None
        self.port = None

        self.title('Ping-Pong')
        self.geometry('300x500')

        CTkLabel(self, text='Connect to server:', font=('Comic Sans MS', 20, 'bold')).pack(pady=15, padx=20, anchor='w')


        self.host_entry = CTkEntry(self, placeholder_text='Введіть хост: ', height=50)
        self.host_entry.pack(padx=20, pady=15, anchor='w', fill='x')

        self.port_entry = CTkEntry(self, placeholder_text='Введіть порт сервера: ', height=50)
        self.port_entry.pack(padx=20, anchor='w', fill='x')

        CTkButton(self, text='Приєднатися', command=self.open_game, height=50).pack(pady=15, padx=20, fill='x')

    def open_game(self):
        self.host = self.host_entry.get()
        self.port = int(self.port_entry.get())
        self.destroy()