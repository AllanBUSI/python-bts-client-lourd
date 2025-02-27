import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.pack(pady=5)

        tk.Label(self, text="Mot de passe:").pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self, text="Se connecter", command=self.login).pack(pady=5)
        tk.Button(self, text="S'inscrire", command=self.register).pack(pady=5)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        conn = sqlite3.connect("app_kanban.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.controller.set_current_user(user[0])
            self.controller.show_frame("BoardPage")
        else:
            messagebox.showerror("Erreur", "Identifiants invalides.")

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        conn = sqlite3.connect("app_kanban.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            messagebox.showinfo("Succès", "Inscription réussie !")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Cet email est déjà enregistré.")
        conn.close()
