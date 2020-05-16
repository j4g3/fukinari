from requests import post
from tkinter import *
from tkinter import messagebox
import sys
import requests
import json

class Gui():
    def main(self):
        self.root = Tk()
        label = Label(self.root, text='Bot token')
        confirmBtn = Button(self.root, text='Login', command=lambda: self.validate())
        self.tokenE = Entry(self.root, width=50)
        self.tokenE.pack()
        label.pack()
        confirmBtn.pack()
        self.root.quit()
        self.root.mainloop()
        self.root.quit()
    def validate(self):
        self.token = self.tokenE.get()
        self.bye()
    def bye(self):
        self.root.destroy()

