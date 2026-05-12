import json
import datetime
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import  *

DATA_FILE = "data_movies.json"

class MovieLibrary:
    def __init__(self, root): #инициализация и задание GUI
        self.root = root
        self.root.title("Movie Library ")
        self.root.geometry("800x500")
        self.movies = []
        self.load_from_JSON()
        input_frame = ttk.LabelFrame(root, text="Добавить фильм")
        input_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5)   
        self.genre_entry = ttk.Entry(input_frame, width=20) 
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5)  
        self.rating_entry = ttk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
        add_btn = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=1, column=4, padx=10, pady=5)
        filter_frame = ttk.LabelFrame(root, text="Фильтрация")
        filter_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre = ttk.Entry(filter_frame, width=20)  
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="Год выпуска:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_year = ttk.Entry(filter_frame, width=10)
        self.filter_year.grid(row=0, column=3, padx=5, pady=5)    
        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=10, pady=5)
        reset_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)  
        reset_btn.grid(row=0, column=5, padx=5, pady=5)
        self.tree = ttk.Treeview(root, columns=("name", "genre", "year", "rating"), show="headings")
        self.tree.heading("name", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год") 
        self.tree.heading("rating", text="Рейтинг")  
        self.tree.column("name", width=250)
        self.tree.column("genre", width=150)   
        self.tree.column("year", width=80)  
        self.tree.column("rating", width=80)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        del_btn = ttk.Button(root, text="Удалить выбранный фильм", command=self.delete_movie)
        del_btn.pack(pady=5)
        self.refresh_table()
    def load_from_JSON (self): #Загрузка данных из JSON-файла
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f) 
        else:
            self.movies = []
    def push_to_JSON (self): #выгрузка данных в JSON-файл
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
    def is_correct(self, name, genre, year_str, rating_str): #Проверка на корректность 
        if not name or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны")
            return False
        try:
            year = int(year_str)
            if year < 1894 or year > datetime.date.today().year:
                cur_year = "Год должен быть от 1894 до " + str(datetime.date.today().year)
                messagebox.showerror("Ошибка", cur_year)
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return False
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return False
        return True
    def add_movie(self): #добавление фильма
        name = self.name_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()
        if self.is_correct(name, genre, year_str, rating_str):
            movie = {
                "name": name,
                "genre": genre,
                "year": int(year_str),
                "rating": round(float(rating_str), 5)
            }
            self.movies.append(movie)
            self.push_to_JSON()
            self.refresh_table()
            self.name_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)
    def delete_movie(self): #удаление фильмов
        random_click_defense = askyesno(title="Подтверждение", message="Вы уверены, что хотите удалить данные о выбранных фильмах?")
        if not(random_click_defense): showinfo("Результат", "Операция отменена")
        else: 
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите фильм для удаления")
                return
            for k in range(len(selected)) :
                item = self.tree.item(selected[k])
                #print(item)
                values = item["values"]
                for i, m in enumerate(self.movies):
                    #print(m["name"] == values[0] , values[1] , m["year"] == values[2] , float(m["rating"]) - float(values[3]) <= 0.0000001)
                    if str(m["name"]) == str(values[0]) and str(m["genre"]) == str(values[1]) and m["year"] == values[2] and float(m["rating"]) - float(values[3]) <= 0.0000001:
                        del self.movies[i]
                        break
            self.push_to_JSON()
            self.refresh_table()
            showinfo("Результат", "Успешно удалено!")
    def refresh_table(self, filtered_movies=None): #Обновление данных на таблице
        self.load_from_JSON()
        for row in self.tree.get_children():
            self.tree.delete(row)
        movies_to_show = filtered_movies if filtered_movies is not None else self.movies
        for m in movies_to_show:  
            self.tree.insert("", tk.END, values=(m["name"], m["genre"], m["year"], m["rating"]))
    def apply_filter(self): #работа с фильтрами
        genre = self.filter_genre.get().strip().lower()
        year_str = self.filter_year.get().strip()
        filtered = self.movies[:]   
        if genre:
            filtered = [m for m in filtered if genre in m["genre"].lower()]
        if year_str:
            try:
                year = int(year_str)
                filtered = [m for m in filtered if m["year"] == year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом")
                return
        self.refresh_table(filtered)
    def reset_filter(self): #очистка фильтров
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
