import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Frame centrale
        frame = tk.Frame(self, bg="white", padx=200, pady=20, relief="ridge", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        tk.Label(frame, text="Connexion", font=("Arial", 16, "bold"), bg="white", fg="#111827").pack(pady=(0, 10))

        # Champ Email
        tk.Label(frame, text="Adresse e-mail", font=("Arial", 10), bg="white", fg="#6b7280").pack(anchor="w")
        self.entry_email = tk.Entry(frame, font=("Arial", 12), bg="#f9fafb", fg="#111827", relief="flat", bd=2)
        self.entry_email.pack(fill="x", padx=5, pady=5, ipady=5)
        
        # Champ Mot de passe
        tk.Label(frame, text="Mot de passe", font=("Arial", 10), bg="white", fg="#6b7280").pack(anchor="w")
        self.entry_password = tk.Entry(frame, font=("Arial", 12), bg="#f9fafb", fg="#111827", relief="flat", bd=2, show="*")
        self.entry_password.pack(fill="x", padx=5, pady=5, ipady=5)

        # Bouton Se connecter
        self.btn_login = tk.Button(frame, text="Se connecter", font=("Arial", 12, "bold"), bg="#3b82f6", fg="white",
            relief="flat", bd=0, activebackground="#2563eb", activeforeground="white",
            command=self.login)
        self.btn_login.pack(fill="x", pady=10, ipady=5)

        # Bouton S'inscrire
        self.btn_register = tk.Button(frame, text="S'inscrire", font=("Arial", 12, "bold"), bg="#10b981", fg="white",
            relief="flat", bd=0, activebackground="#059669", activeforeground="white",
            command=self.register)
        self.btn_register.pack(fill="x", ipady=5)
        

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
