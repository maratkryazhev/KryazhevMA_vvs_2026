import tkinter as tk
from tkinter import ttk, messagebox
import validators
import matrix_operations
import properties

class MatrixCalculatorTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Матричный калькулятор (Tkinter)')
        self.geometry('900x750')
        
        # Переменные для хранения текущих настроек
        self.operation_var = tk.StringVar(value='Сложение')
        self.size_var = tk.IntVar(value=3)
        
        self.entries_A = []
        self.entries_B = []
        
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # ВЕРХНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ
        control_frame = tk.Frame(self, pady=10)
        control_frame.pack(fill='x')

        tk.Label(control_frame, text='Операция:', font=('Arial', 12)).pack(side='left', padx=5)
        
        operations = [
            'Сложение', 'Умножение матриц', 'Умножение на число', 
            'Транспонирование', 'Обратная матрица', 'Определитель',
            'Единичная матрица', 'Нулевая матрица', 'Главная диагональ'
        ]
        
        op_menu = ttk.Combobox(control_frame, textvariable=self.operation_var, values=operations, state='readonly', width=20)
        op_menu.pack(side='left', padx=5)
        op_menu.bind('<<ComboboxSelected>>', lambda e: self.update_ui())

        tk.Label(control_frame, text='Размер (NxN):', font=('Arial', 12)).pack(side='left', padx=(20, 5))
        size_spin = ttk.Spinbox(control_frame, from_=1, to=5, textvariable=self.size_var, width=5, state='readonly')
        size_spin.pack(side='left', padx=5)
        size_spin.bind('<<Increment>>', lambda e: self.update_ui())
        size_spin.bind('<<Decrement>>', lambda e: self.update_ui())

        # ЦЕНТРАЛЬНАЯ ЧАСТЬ (МАТРИЦЫ И ВВОД)
        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # НИЖНЯЯ ЧАСТЬ (КНОПКИ И РЕЗУЛЬТАТ)
        bottom_frame = tk.Frame(self, pady=10)
        bottom_frame.pack(fill='x', side='bottom')

        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack()
        
        tk.Button(btn_frame, text='ВЫЧИСЛИТЬ', command=self.calculate, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='ПОКАЗАТЬ СВОЙСТВА', command=self.show_properties, bg='#2196F3', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text='ОЧИСТИТЬ', command=self.update_ui, bg='#f44336', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=10)

        self.result_text = tk.Text(self, height=10, font=('Courier', 12), bg='#f0f0f0')
        self.result_text.pack(fill='x', padx=20, pady=(0, 20))

    def create_matrix_grid(self, parent, title, prefix):
        frame = tk.LabelFrame(parent, text=title, font=('Arial', 12, 'bold'), padx=10, pady=10)
        frame.pack(side='left', expand=True, padx=20)
        
        entries = []
        size = self.size_var.get()
        
        for i in range(size):
            row_entries = []
            for j in range(size):
                e = tk.Entry(frame, width=5, font=('Arial', 12), justify='center')
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            entries.append(row_entries)
        return entries

    def update_ui(self):
        # Очищаем старую отрисовку
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_text.delete('1.0', tk.END)
        
        op = self.operation_var.get()
        size = self.size_var.get()

        # Логика отрисовки полей в зависимости от операции
        if op in ['Сложение', 'Умножение матриц']:
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A', 'A')
            self.entries_B = self.create_matrix_grid(self.matrix_frame, 'Матрица B', 'B')
            
        elif op == 'Умножение на число':
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A', 'A')
            scalar_frame = tk.Frame(self.matrix_frame)
            scalar_frame.pack(side='left', padx=20)
            tk.Label(scalar_frame, text='Число (k):', font=('Arial', 12, 'bold')).pack()
            self.scalar_entry = tk.Entry(scalar_frame, width=10, font=('Arial', 12))
            self.scalar_entry.pack(pady=10)
            
        elif op in ['Транспонирование', 'Обратная матрица', 'Определитель', 'Главная диагональ']:
            self.entries_A = self.create_matrix_grid(self.matrix_frame, 'Матрица A', 'A')
            
        elif op in ['Единичная матрица', 'Нулевая матрица']:
            tk.Label(self.matrix_frame, text=f"Нажмите 'ВЫЧИСЛИТЬ', чтобы сгенерировать матрицу {size}x{size}", font=('Arial', 14)).pack(expand=True)

    def get_matrix_from_entries(self, entries):
        raw_data = []
        for row in entries:
            raw_data.append([e.get() for e in row])
        return validators.parse_matrix(raw_data)

    def format_matrix(self, matrix):
        # Красивый вывод матрицы в текстовое поле
        lines = []
        for row in matrix:
            row_str = '  '.join(f"{val:8.2f}" for val in row)
            lines.append(f"[ {row_str} ]")
        return "\n".join(lines)

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
                return
                
            elif op == 'Главная диагональ':
                validators.check_square(A)
                diag = matrix_operations.get_main_diagonal(A)
                self.result_text.insert(tk.END, f"Элементы главной диагонали:\n{diag}")
                return

            self.result_text.insert(tk.END, "Результат:\n")
            self.result_text.insert(tk.END, self.format_matrix(res))

        except validators.MatrixError as e:
            messagebox.showerror('Ошибка валидации', str(e))
        except Exception as e:
            messagebox.showerror('Неизвестная ошибка', f"Что-то пошло не так:\n{str(e)}")

    def show_properties(self):
        # Вывод свойств в отдельном диалоговом окне
        prop_window = tk.Toplevel(self)
        prop_window.title('Свойства операций')
        prop_window.geometry('600x500')
        
        text = tk.Text(prop_window, wrap='word', font=('Arial', 11))
        text.pack(expand=True, fill='both', padx=10, pady=10)
        
        all_props = f"{properties.PROPERTIES_ADD_SCALAR}\n\n" \
                    f"{properties.PROPERTIES_MULTIPLICATION}\n\n" \
                    f"{properties.PROPERTIES_INVERSE}"
        
        text.insert(tk.END, all_props)
        text.config(state='disabled')

if __name__ == '__main__':
    app = MatrixCalculatorTk()
    app.mainloop()
