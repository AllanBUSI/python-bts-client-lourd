import tkinter as tk
from tkinter import messagebox
import sqlite3
from DragLabel import DragLabel

class BoardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F9FAFB")  # Fond clair style Tailwind
        self.controller = controller
        self.drag_labels = []

        # Configuration responsive des colonnes
        self.column_frames = {}
        self.create_columns()

        # Bouton Nouvelle Tâche
        self.new_task_button = tk.Button(
            self,
            text="➕ Nouvelle tâche",
            command=self.open_new_task_window,
            bg="#3B82F6",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )
        self.new_task_button.pack(pady=10, anchor="center")

        # Recharge les tâches quand visible
        self.bind("<Visibility>", lambda e: self.load_tasks())

        # Responsive
        self.bind("<Configure>", self.responsive_columns)

    def create_columns(self):
        statuses = [("todo", "📝 À faire", "#FEE2E2"),
                    ("doing", "🚧 En cours", "#FEF9C3"),
                    ("done", "✅ Fini", "#D1FAE5")]

        for status, label, color in statuses:
            frame = tk.Frame(self, bg=color, relief="ridge", borderwidth=5)
            title = tk.Label(
                frame, text=label,
                font=("Arial", 14, "bold"), bg=color
            )
            title.pack(pady=10)
            self.column_frames[status] = frame
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def responsive_columns(self, event=None):
        width = self.winfo_width()
        side = tk.LEFT if width > 600 else tk.TOP
        for frame in self.column_frames.values():
            frame.pack_forget()
            frame.pack(side=side, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_tasks(self):
        for frame in self.column_frames.values():
            for widget in frame.winfo_children():
                if isinstance(widget, DragLabel):
                    widget.destroy()
        self.drag_labels.clear()

        conn = sqlite3.connect("app_kanban.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status FROM tasks WHERE user_id=?", (self.controller.current_user_id,))
        tasks = cursor.fetchall()
        conn.close()

        for task_id, title, description, status in tasks:
            self.create_task_label(task_id, title, description, status)

    def create_task_label(self, task_id, title, description, status):
        label = DragLabel(
            parent=self.column_frames[status],
            task_id=task_id,
            title=title,
            status=status,
            user_id=self.controller.current_user_id,
            on_drop_callback=self.on_task_drop,
            text=f"{title}\n{description}",
            bg="white",
            fg="#374151",
            font=("Arial", 11),
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            justify="left"
        )
        # Attribut personnalisé ajouté après création
        label.description = description

        label.pack(pady=5, padx=10, fill="x")
        self.drag_labels.append(label)


    def open_new_task_window(self):
        new_task_win = tk.Toplevel(self)
        new_task_win.title("Ajouter une nouvelle tâche")
        new_task_win.configure(bg="#F9FAFB")

        tk.Label(new_task_win, text="Titre de la tâche :", bg="#F9FAFB", font=("Arial", 12)).pack(pady=5)
        entry_title = tk.Entry(new_task_win, font=("Arial", 12), width=30)
        entry_title.pack(pady=5)

        tk.Label(new_task_win, text="Description :", bg="#F9FAFB", font=("Arial", 12)).pack(pady=5)
        entry_description = tk.Text(new_task_win, font=("Arial", 12), height=5, width=30)
        entry_description.pack(pady=5)

        tk.Button(
            new_task_win,
            text="Ajouter",
            command=lambda: self.add_task(entry_title, entry_description, new_task_win),
            bg="#10B981",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=10,
            pady=5
        ).pack(pady=10)

    def add_task(self, entry_title, entry_description, window):
        title = entry_title.get().strip()
        description = entry_description.get("1.0", tk.END).strip()
        if not title:
            messagebox.showerror("Erreur", "Veuillez entrer un titre.")
            return
        conn = sqlite3.connect("app_kanban.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?,?,?)",
                       (title, description,'todo', self.controller.current_user_id))
        conn.commit()
        conn.close()
        window.destroy()
        self.load_tasks()

    def on_task_drop(self, task_id, x_root, y_root):
        for status, frame in self.column_frames.items():
            x, y, w, h = frame.winfo_rootx(), frame.winfo_rooty(), frame.winfo_width(), frame.winfo_height()
            if x < x_root < x + w and y < y_root < y + h:
                conn = sqlite3.connect("app_kanban.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
                conn.commit()
                conn.close()
                self.load_tasks()
                return
        self.load_tasks()
