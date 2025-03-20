import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import BoardPage
import LoginPage

# ============= CREATION DE LA BD ET DES TABLES ============= #

conn = sqlite3.connect("app_kanban.db")
cursor = conn.cursor()

# Table des utilisateurs
cursor.execute('''\
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

# Table des taches
cursor.execute('''\
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,  -- 'todo', 'doing', 'done'
    user_id INTEGER,
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

conn.commit()
conn.close()

# =============================================== #

class KanbanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Kanban - BTS SIO SLAM")
        self.geometry("800x600")

        # Conteneur de pages (frames)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage.LoginPage, BoardPage.BoardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")
        self.current_user_id = None

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_current_user(self, user_id):
        self.current_user_id = user_id




if __name__ == "__main__":
    app = KanbanApp()
    app.mainloop()
