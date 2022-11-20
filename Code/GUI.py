import tkinter as tk
from tkinter import filedialog, Text
import os

def search():
    query = searchBar.get()
    print(query)

root = tk.Tk()

canvas = tk.Canvas(root, height=500, width=350, bg="#263D42")
canvas.pack() # Adds the canvas to the root

searchBar = tk.Entry(root)
canvas.create_window(100, 40, window=searchBar)

searchButton = tk.Button(root, text="Ask Alfred", command=search)
searchButton.pack()

root.mainloop()