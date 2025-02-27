import tkinter as tk

class DragLabel(tk.Label):
    """Label personnalisée pour le drag & drop"""
    def __init__(self, parent, task_id, title, status, user_id, on_drop_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.task_id = task_id
        self.title = title
        self.status = status
        self.user_id = user_id
        self.on_drop_callback = on_drop_callback

        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind("<ButtonRelease-1>", self.on_drag_release)

        self._drag_start_x = 0
        self._drag_start_y = 0

    def on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag_motion(self, event):
        x = self.winfo_x() - self._drag_start_x + event.x
        y = self.winfo_y() - self._drag_start_y + event.y
        self.place(x=x, y=y)  # on deplace la tache

    def on_drag_release(self, event):
        # callback pour re-categoriser la tache en fonction de la frame dans laquelle elle est lachée
        self.on_drop_callback(self.task_id, event.x_root, event.y_root)
