import tkinter as tk
from tkinter import messagebox
import sqlite3
from DragLabel import DragLabel

class BoardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # 3 zones: A faire, En cours, Fini
        self.column_frames = {}
        self.column_frames["todo"] = tk.Frame(self, bg="#FFD5D5", width=200, height=500)
        self.column_frames["todo"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.column_frames["doing"] = tk.Frame(self, bg="#FFFCD5", width=200, height=500)
        self.column_frames["doing"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.column_frames["done"] = tk.Frame(self, bg="#D5FFD5", width=200, height=500)
        self.column_frames["done"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Titres
        tk.Label(self.column_frames["todo"], text="A faire", font=("Arial", 14, "bold"), bg="#FFD5D5").pack(pady=5)
        tk.Label(self.column_frames["doing"], text="En cours", font=("Arial", 14, "bold"), bg="#FFFCD5").pack(pady=5)
        tk.Label(self.column_frames["done"], text="Fini", font=("Arial", 14, "bold"), bg="#D5FFD5").pack(pady=5)

        # Bouton pour créer une nouvelle tache
        self.new_task_button = tk.Button(self, text="Nouvelle tache", command=self.open_new_task_window)
        self.new_task_button.place(x=10, y=10)

        # On charge les taches quand la page s'affiche
        self.bind("<Visibility>", lambda e: self.load_tasks())

        # On stocke toutes les labels drag & drop pour eviter qu'elles soient garbage-collected
        self.drag_labels = []

    def load_tasks(self):
        # Effacer ce qui existe dans les colonnes
        for col in self.column_frames:
            for widget in self.column_frames[col].winfo_children():
                if isinstance(widget, DragLabel):
                    widget.destroy()
        self.drag_labels.clear()

        # Charger depuis la base de données
        conn = sqlite3.connect("app_kanban.db")
        cursor = conn.cursor()
        # Charger les taches de l'utilisateur en cours
        user_id = self.controller.current_user_id
        cursor.execute("SELECT id, title, status FROM tasks WHERE user_id=?", (user_id,))
        tasks = cursor.fetchall()
        conn.close()

        # Creer les labels pour chaque tache
        for (task_id, title, status) in tasks:
            self.create_task_label(task_id, title, status)

    def create_task_label(self, task_id, title, status):
        label = DragLabel(
            parent=self.column_frames[status],
            task_id=task_id,
            title=title,
            status=status,
            user_id=self.controller.current_user_id,
            on_drop_callback=self.on_task_drop,
            text=title,
            bg="white",
            bd=1,
            relief="solid",
            padx=5,
            pady=5
        )
        label.pack(pady=5, padx=5, anchor="n")
        self.drag_labels.append(label)

    def open_new_task_window(self):
        new_task_win = tk.Toplevel(self)
        new_task_win.title("Nouvelle tâche")

        tk.Label(new_task_win, text="Titre de la tâche:").pack(pady=5)
        entry_title = tk.Entry(new_task_win)
        entry_title.pack(pady=5)

        def add_task():
            title = entry_title.get()
            if not title:
                messagebox.showerror("Erreur", "Titre vide.")
                return
            conn = sqlite3.connect("app_kanban.db")
            cursor = conn.cursor()
            # Par defaut, on ajoute dans la colonne "A faire" (todo)
            cursor.execute("INSERT INTO tasks (title, status, user_id) VALUES (?, ?, ?)", (title, "todo", self.controller.current_user_id))
            conn.commit()
            conn.close()
            new_task_win.destroy()
            self.load_tasks()

        tk.Button(new_task_win, text="Ajouter", command=add_task).pack(pady=5)

    def on_task_drop(self, task_id, x_root, y_root):
        # Determiner dans quel cadre la tache a ete lachee en fonction de x_root, y_root
        # On recupere la position de chaque frame
        for status, frame in self.column_frames.items():
            # Obtenir la position absolue de la frame
            frame_x = frame.winfo_rootx()
            frame_y = frame.winfo_rooty()
            frame_w = frame.winfo_width()
            frame_h = frame.winfo_height()

            # Verifier si x_root, y_root est dans le rectangle de la frame
            if frame_x < x_root < frame_x + frame_w and frame_y < y_root < frame_y + frame_h:
                # On met a jour le status de la tache
                conn = sqlite3.connect("app_kanban.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
                conn.commit()
                conn.close()
                self.load_tasks()
                return

        # Si la tache n'est pas droppée dans une zone, on la remet a jour
        self.load_tasks()
