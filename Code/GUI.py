import tkinter
import customtkinter

def startup():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("300x400")
    app.title("Alfred")

    app.mainloop()