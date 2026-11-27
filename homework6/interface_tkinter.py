import tkinter as tk
from tkinter import ttk, messagebox
import threading

import validators
import matrix_operations
import properties
from BD import DBWorker
from schemes import User

BG_COLOR = "#000000"
FG_COLOR = "#00FF00"
ACCENT_COLOR = "#001100"
INPUT_BG = "#002200"

# ОКНО АВТОРИЗАЦИИ
class AuthWindow(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.uid = None
        self.title('Авторизация')
        self.geometry('320x220')
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='Логин:', bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12)).pack(pady=(15, 5))
        self.user_entry = tk.Entry(self, bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, font=('Courier New', 12))
        self.user_entry.pack()

        tk.Label(self, text='Пароль:', bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12)).pack(pady=(10, 5))
        self.pass_entry = tk.Entry(self, show="*", bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, font=('Courier New', 12))
        self.pass_entry.pack()

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text='Войти', command=self.login, bg=INPUT_BG, fg=FG_COLOR, font=('Courier New', 11, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='Регистрация', command=self.register, bg=INPUT_BG, fg=FG_COLOR, font=('Courier New', 11, 'bold')).pack(side='left', padx=10)

    def login(self):
        name = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if not name or not pwd:
            messagebox.showerror('Ошибка', 'Заполните все поля!')
            return
        try:
            self.uid = self.db.check_cred(name, pwd)
            self.destroy()
        except Exception as e:
            messagebox.showerror('Ошибка авторизации', str(e))

    def register(self):
        name = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if not name or not pwd:
            messagebox.showerror('Ошибка', 'Заполните все поля!')
            return
        
        user = User(name=name, email=f"{name}@matrix.ru", passwd=pwd)
        if self.db.add_user(user):
            messagebox.showinfo('Успех', 'Аккаунт создан! Теперь войдите.')
        else:
            messagebox.showerror('Ошибка', 'Такое имя уже занято.')

# ГЛАВНОЕ ОКНО КАЛЬКУЛЯТОРА
class MatrixCalculatorTk(tk.Tk):
    def __init__(self, db: DBWorker, uid: int):
        super().__init__()
        self.db = db
        self.uid = uid
        self.title('Матричный калькулятор (Tkinter + БД)')
        self.geometry('950x850')
        self.configure(bg=BG_COLOR)
        
        self.operation_var = tk.StringVar(value='Сложение')
        self.size_var = tk.IntVar(value=3)
        
        self.entries_A = []
        self.entries_B = []
        
        self.create_widgets()
        self.update_ui()
        self.refresh_stats()

    def create_widgets(self):
        # ВЕРХНЯЯ ПАНЕЛЬ
        stats_frame = tk.Frame(self, bg=BG_COLOR)
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_label = tk.Label(stats_frame, text='⚡ Энергия: загрузка...', bg=BG_COLOR, fg='#FFFF00', font=('Courier New', 14, 'bold'))
        self.stats_label.pack(side='left', padx=20)

        # ПАНЕЛЬ УПРАВЛЕНИЯ
        control_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        control_frame.pack(fill='x')

        tk.Label(control_frame, text='Операция:', bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12)).pack(side='left', padx=5)
        
        operations = [
            'Сложение', 'Умножение матриц', 'Умножение на число', 
            'Транспонирование', 'Обратная матрица', 'Определитель',
            'Единичная матрица', 'Нулевая матрица', 'Главная диагональ'
        ]
        
        op_menu = ttk.Combobox(control_frame, textvariable=self.operation_var, values=operations, state='readonly', width=20, font=('Courier New', 11))
        op_menu.pack(side='left', padx=5)
        op_menu.bind('<<ComboboxSelected>>', lambda e: self.update_ui())

        tk.Label(control_frame, text='Размер (NxN):', bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12)).pack(side='left', padx=(20, 5))
        size_spin = tk.Spinbox(control_frame, from_=1, to=5, textvariable=self.size_var, width=5, state='readonly', font=('Courier New', 11))
        size_spin.pack(side='left', padx=5)
        size_spin.bind('<<Increment>>', lambda e: self.update_ui())
        size_spin.bind('<<Decrement>>', lambda e: self.update_ui())

        # ЦЕНТРАЛЬНАЯ ЧАСТЬ (МАТРИЦЫ И ВВОД)
        self.matrix_frame = tk.Frame(self, bg=BG_COLOR)
        self.matrix_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # НИЖНЯЯ ЧАСТЬ (КНОПКИ И РЕЗУЛЬТАТ)
        bottom_frame = tk.Frame(self, pady=10, bg=BG_COLOR)
        bottom_frame.pack(fill='x', side='bottom')

        btn_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
        btn_frame.pack()
        
        tk.Button(btn_frame, text='ВЫЧИСЛИТЬ', command=self.calculate, bg=INPUT_BG, fg=FG_COLOR, font=('Courier New', 12, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='СВОЙСТВА', command=self.show_properties, bg=INPUT_BG, fg=FG_COLOR, font=('Courier New', 12, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='ОЧИСТИТЬ', command=self.update_ui, bg=INPUT_BG, fg=FG_COLOR, font=('Courier New', 12, 'bold')).pack(side='left', padx=10)

        self.result_text = tk.Text(self, height=10, font=('Courier New', 14), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
        self.result_text.pack(fill='x', padx=20, pady=(0, 20))

    def create_matrix_grid(self, parent, title):
        frame = tk.LabelFrame(parent, text=title, font=('Courier New', 12, 'bold'), bg=BG_COLOR, fg=FG_COLOR, bd=2, relief='solid')
        frame.pack(side='left', expand=True, padx=20)
        
        entries = []
        size = self.size_var.get()
        
        for i in range(size):
            row_entries = []
            for j in range(size):
                e = tk.Entry(frame, width=5, font=('Courier New', 12), justify='center', bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            entries.append(row_entries)
        return entries

    def update_ui(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_text.delete('1.0', tk.END)
        
        op = self.operation_var.get()
        size = self.size_var.get()

        if op in ['Сложение', 'Умножение матриц']:
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A')
            self.entries_B = self.create_matrix_grid(self.matrix_frame, 'Матрица B')
            
        elif op == 'Умножение на число':
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A')
            scalar_frame = tk.Frame(self.matrix_frame, bg=BG_COLOR)
            scalar_frame.pack(side='left', padx=20)
            tk.Label(scalar_frame, text='Число (k):', bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12, 'bold')).pack()
            self.scalar_entry = tk.Entry(scalar_frame, width=10, font=('Courier New', 12), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
            self.scalar_entry.pack(pady=10)
            
        elif op in ['Транспонирование', 'Обратная матрица', 'Определитель', 'Главная диагональ']:
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A')
            
        elif op in ['Единичная матрица', 'Нулевая матрица']:
            tk.Label(self.matrix_frame, text=f"Нажмите 'ВЫЧИСЛИТЬ', чтобы сгенерировать матрицу {size}x{size}", bg=BG_COLOR, fg=FG_COLOR, font=('Courier New', 12)).pack(expand=True)

    def get_matrix_from_entries(self, entries):
        raw_data = []
        for row in entries:
            raw_data.append([e.get() for e in row])
        return validators.parse_matrix(raw_data)

    def format_matrix(self, matrix):
        lines = []
        for row in matrix:
            row_str = '  '.join(f"{val:8.2f}" for val in row)
            lines.append(f"[ {row_str} ]")
        return "\n".join(lines)

    # РАБОТА С БД (В ФОНЕ)
    def refresh_stats(self):
        # Запрашивает стату из БД в отдельном потоке, чтобы окно не зависало
        def fetch():
            stats = self.db.get_stats(self.uid)
            # Возвращаемся в главный поток для обновления UI
            self.after(0, lambda: self.update_stats_ui(stats))
            
        threading.Thread(target=fetch, daemon=True).start()

    def update_stats_ui(self, stats):
        energy, ops = stats
        self.stats_label.config(text=f"⚡ Энергия: {energy} | 🧮 Операций: {ops}")

    def on_success_calc(self):
        # Начисляет энергию в фоне
        def add():
            self.db.add_energy(self.uid, 10)
            self.refresh_stats()
            
        threading.Thread(target=add, daemon=True).start()

    # ЛОГИКА КАЛЬКУЛЯТОРА
    def calculate(self):
        op = self.operation_var.get()
        size = self.size_var.get()
        self.result_text.delete('1.0', tk.END)

        try:
            if op in ['Единичная матрица', 'Нулевая матрица']:
                if op == 'Единичная матрица':
                    res = matrix_operations.get_identity(size)
                else:
                    res = matrix_operations.get_zero(size, size)
                self.result_text.insert(tk.END, self.format_matrix(res))
                self.on_success_calc()
                return

            A = self.get_matrix_from_entries(self.entries_A)

            if op == 'Сложение':
                B = self.get_matrix_from_entries(self.entries_B)
                validators.check_same_size(A, B)
                res = matrix_operations.add_matrices(A, B)
                
            elif op == 'Умножение матриц':
                B = self.get_matrix_from_entries(self.entries_B)
                validators.check_multiplication(A, B)
                res = matrix_operations.multiply_matrices(A, B)
                
            elif op == 'Умножение на число':
                scalar = validators.check_scalar(self.scalar_entry.get())
                res = matrix_operations.multiply_by_scalar(A, scalar)
                
            elif op == 'Транспонирование':
                res = matrix_operations.transpose(A)
                
            elif op == 'Обратная матрица':
                validators.check_square(A)
                res = matrix_operations.inverse_matrix(A)
                
            elif op == 'Определитель':
                validators.check_square(A)
                det = matrix_operations.get_determinant(A)
                self.result_text.insert(tk.END, f"Определитель матрицы A:\ndet(A) = {det:.4f}")
                self.on_success_calc()
                return
                
            elif op == 'Главная диагональ':
                validators.check_square(A)
                diag = matrix_operations.get_main_diagonal(A)
                self.result_text.insert(tk.END, f"Элементы главной диагонали:\n{diag}")
                self.on_success_calc()
                return

            self.result_text.insert(tk.END, "Результат:\n")
            self.result_text.insert(tk.END, self.format_matrix(res))
            self.on_success_calc()

        except validators.MatrixError as e:
            messagebox.showerror('Ошибка валидации', str(e))
        except Exception as e:
            messagebox.showerror('Неизвестная ошибка', f"Что-то пошло не так:\n{str(e)}")

    def show_properties(self):
        prop_window = tk.Toplevel(self)
        prop_window.title('Свойства операций')
        prop_window.geometry('600x500')
        prop_window.configure(bg=BG_COLOR)
        
        text = tk.Text(prop_window, wrap='word', font=('Courier New', 11), bg=INPUT_BG, fg=FG_COLOR)
        text.pack(expand=True, fill='both', padx=10, pady=10)
        
        all_props = f"{properties.PROPERTIES_ADD_SCALAR}\n\n" \
                    f"{properties.PROPERTIES_MULTIPLICATION}\n\n" \
                    f"{properties.PROPERTIES_INVERSE}"
        
        text.insert(tk.END, all_props)
        text.config(state='disabled')

# ТОЧКА ВХОДА
if __name__ == '__main__':
    db = DBWorker()
    
    # 1. Запускаем окно авторизации как самостоятельное главное окно
    auth_window = AuthWindow(db)
    auth_window.mainloop()
    
    # 2. Проверяем, вошел ли пользователь (остался ли uid)
    if auth_window.uid is not None:
        # 3. Создаем калькулятор ТОЛЬКО после того, как окно авторизации полностью уничтожено
        app = MatrixCalculatorTk(db, auth_window.uid)
        app.mainloop()
