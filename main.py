import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Константы
FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://github.com"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")

        # --- UI Элементы ---
        self.label = tk.Label(root, text="Введите имя пользователя GitHub:", font=("Arial", 10))
        self.label.pack(pady=10)

        self.search_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Найти", command=self.search_user, bg="#2ea44f", fg="white")
        self.search_button.pack(pady=5)

        self.result_box = tk.Text(root, height=10, width=40, state='disabled', font=("Arial", 10))
        self.result_box.pack(pady=10)

        self.fav_button = tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites, state='disabled')
        self.fav_button.pack(pady=5)

        self.view_fav_button = tk.Button(root, text="Показать избранное", command=self.show_favorites)
        self.view_fav_button.pack(pady=5)

        self.current_user_data = None

    def search_user(self):
        username = self.search_entry.get().strip()
        
        # Валидация (Критерий 5)
        if not username:
            messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"{GITHUB_API_URL}{username}")
            if response.status_code == 200:
                data = response.json()
                self.current_user_data = {
                    "login": data.get("login"),
                    "name": data.get("name"),
                    "bio": data.get("bio"),
                    "url": data.get("html_url")
                }
                self.display_result(self.current_user_data)
                self.fav_button.config(state='normal')
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден")
                self.clear_result()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема с сетью: {e}")

    def display_result(self, user):
        self.result_box.config(state='normal')
        self.result_box.delete(1.0, tk.END)
        info = f"Логин: {user['login']}\nИмя: {user['name']}\nБио: {user['bio']}\nСсылка: {user['url']}"
        self.result_box.insert(tk.END, info)
        self.result_box.config(state='disabled')

    def clear_result(self):
        self.result_box.config(state='normal')
        self.result_box.delete(1.0, tk.END)
        self.result_box.config(state='disabled')
        self.fav_button.config(state='disabled')

    def add_to_favorites(self):
        if not self.current_user_data:
            return

        # Загрузка существующих (Критерий 4)
        favorites = []
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                try:
                    favorites = json.load(f)
                except json.JSONDecodeError:
                    favorites = []

        # Проверка на дубликаты
        if any(u['login'] == self.current_user_data['login'] for u in favorites):
            messagebox.showinfo("Инфо", "Пользователь уже в избранном")
            return

        favorites.append(self.current_user_data)

        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, indent=4, ensure_ascii=False)
        
        messagebox.showinfo("Успех", f"{self.current_user_data['login']} добавлен в избранное!")

    def show_favorites(self):
        if not os.path.exists(FAVORITES_FILE):
            messagebox.showinfo("Избранное", "Список пуст")
            return

        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            favorites = json.load(f)
            names = "\n".join([u['login'] for u in favorites])
            messagebox.showinfo("Ваше избранное", names if names else "Список пуст")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
