import tkinter as tk
from tkinter import messagebox
import json
import os

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.current_theme = "light"

        self.notes = self.load_notes()

        self.create_widgets()

        self.apply_theme()

    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return []

    def save_notes(self):
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(self.notes, file, indent=4)

    def create_widgets(self):
        self.note_titles_frame = tk.Frame(self.root, width=200, bd=0)
        self.note_titles_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky="ns")

        self.note_listbox = tk.Listbox(self.note_titles_frame, height=25, selectmode=tk.SINGLE, font=("Arial", 12))
        self.note_listbox.pack(fill=tk.BOTH, expand=True)
        self.note_listbox.bind("<<ListboxSelect>>", self.update_selected_note)

        self.note_text_frame = tk.Frame(self.root, bg="#f0f0f0", bd=0)
        self.note_text_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        self.note_text = tk.Text(self.note_text_frame, wrap=tk.WORD, font=("Arial", 12), bg="#f0f0f0", bd=0)
        self.note_text.pack(fill=tk.BOTH, expand=True)
        self.note_text.config(state=tk.DISABLED)

        self.note_buttons_frame = tk.Frame(self.note_text_frame, bg="#f0f0f0", bd=0)
        self.note_buttons_frame.pack(fill=tk.X, pady=5, anchor="n")

        self.edit_button = tk.Button(self.note_buttons_frame, text="Изменить", command=self.enable_editing, width=10, height=1, font=("Arial", 10))
        self.edit_button.pack(side=tk.LEFT, padx=5)
        self.edit_button.config(state=tk.DISABLED)

        self.save_button = tk.Button(self.note_buttons_frame, text="Сохранить", command=self.save_edited_text, width=10, height=1, font=("Arial", 10))
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.save_button.config(state=tk.DISABLED)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.button_frame = tk.Frame(self.root, bg="#f0f0f0", bd=0)
        self.button_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.add_button = tk.Button(self.button_frame, text="Добавить", command=self.add_note, width=8, height=1, font=("Arial", 10))
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Удалить", command=self.delete_note, width=8, height=1, font=("Arial", 10))
        self.delete_button.grid(row=0, column=1, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)

        self.search_label = tk.Label(self.button_frame, text="Поиск:")
        self.search_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = tk.Entry(self.button_frame, width=25)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_notes)

        self.theme_button = tk.Button(self.button_frame, text="Переключить тему", command=self.toggle_theme, width=15, height=1, font=("Arial", 10))
        self.theme_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.update_note_listbox()

    def search_notes(self, event=None):
        query = self.search_entry.get().lower()
        filtered_notes = [note for note in self.notes if query in note['title'].lower()]
        self.update_note_listbox(filtered_notes)

    def update_note_listbox(self, notes=None):
        self.note_listbox.delete(0, tk.END)
        notes = notes or self.notes
        for note in notes:
            self.note_listbox.insert(tk.END, note['title'])

    def add_note(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить заметку")
        add_window.geometry("400x200")

        title_label = tk.Label(add_window, text="Заголовок:")
        title_label.pack(pady=10)

        title_entry = tk.Entry(add_window, width=40)
        title_entry.pack(pady=10)

        def save_note():
            title = title_entry.get()
            if title:
                new_note = {'title': title, 'text': ""}
                self.notes.append(new_note)
                self.save_notes()
                self.update_note_listbox()
                add_window.destroy()
                self.show_notification("Заметка добавлена!")

        save_button = tk.Button(add_window, text="Сохранить", command=save_note)
        save_button.pack(pady=10)

    def update_selected_note(self, event=None):
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            self.display_note_text(selected_note_index[0])
            self.delete_button.config(state=tk.NORMAL)
            self.edit_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)

    def display_note_text(self, index):
        selected_note = self.notes[index]
        self.note_text.config(state=tk.NORMAL)
        self.note_text.delete("1.0", tk.END)
        self.note_text.insert("1.0", selected_note['text'])
        self.note_text.config(state=tk.DISABLED)

    def save_edited_text(self):
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            selected_note = self.notes[selected_note_index[0]]
            selected_note['text'] = self.note_text.get("1.0", tk.END).strip()
            self.save_notes()
            self.show_notification("Заметка сохранена!")
            self.note_text.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.NORMAL)

    def enable_editing(self):
        self.note_text.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.DISABLED)

    def delete_note(self):
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            selected_note_index = selected_note_index[0]
            del self.notes[selected_note_index]
            self.save_notes()
            self.update_note_listbox()
            self.note_text.config(state=tk.DISABLED)
            self.note_text.delete("1.0", tk.END)
            self.show_notification("Заметка удалена!")

    def show_notification(self, message):
        notification = tk.Toplevel(self.root)
        notification.title("Уведомление")
        notification.geometry("300x100")
        notification.configure(bg="#f0f0f0" if self.current_theme == "light" else "#424242")
        notification_label = tk.Label(notification, text=message, font=("Arial", 12), fg="#4CAF50" if self.current_theme == "light" else "#ff9800", bg=notification.cget("bg"))
        notification_label.pack(pady=20)

        def close_notification():
            notification.destroy()

        notification.after(1500, close_notification)

    def apply_theme(self):
        if self.current_theme == "light":
            self.root.configure(bg="#f0f0f0")
            self.note_titles_frame.configure(bg="#ffffff")
            self.note_text.configure(bg="#ffffff", fg="#4f4f4f")
            self.note_listbox.configure(bg="#ffffff", fg="#4f4f4f")
            self.add_button.configure(bg="#4CAF50", fg="white")
            self.delete_button.configure(bg="#f44336", fg="white")
            self.search_entry.configure(bg="#ffffff", fg="#4f4f4f")
            self.theme_button.configure(bg="#2196F3", fg="white")
            self.button_frame.configure(bg="#f0f0f0")
            self.note_buttons_frame.configure(bg="#f0f0f0")
            self.note_text_frame.configure(bg="#f0f0f0")
            self.save_button.configure(bg="#FF9800", fg="white")
            self.edit_button.configure(bg="#4CAF50", fg="white")
        else:
            self.root.configure(bg="#2c2c2c")
            self.note_titles_frame.configure(bg="#3b3b3b")
            self.note_text.configure(bg="#424242", fg="#bdbdbd")
            self.note_listbox.configure(bg="#424242", fg="#bdbdbd")
            self.add_button.configure(bg="#ff9800", fg="white")
            self.delete_button.configure(bg="#f44336", fg="white")
            self.search_entry.configure(bg="#616161", fg="#bdbdbd")
            self.theme_button.configure(bg="#2196F3", fg="white")
            self.button_frame.configure(bg="#2c2c2c")
            self.note_buttons_frame.configure(bg="#424242")
            self.note_text_frame.configure(bg="#424242")
            self.save_button.configure(bg="#FF9800", fg="white")
            self.edit_button.configure(bg="#4CAF50", fg="white")

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.apply_theme()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
