import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, 
                             QPushButton, QTextEdit, QMessageBox, QDialog, QTextBrowser,
                             QHeaderView, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

import validators
import matrix_operations
import properties

MATRIX_STYLE = '''
QWidget {
    background-color: #000000;
    color: #00FF00;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    font-weight: bold;
}
QLabel {
    color: #00FF00;
}
QComboBox, QSpinBox, QTextEdit {
    background-color: #001100;
    border: 2px solid #00FF00;
    color: #00FF00;
    padding: 2px;
}
QTableWidget {
    background-color: #001100;
    border: 2px solid #00FF00;
    gridline-color: #00FF00;
}
QTableWidget::item {
    border: 1px solid #005500;
    padding: 5px;
}
QPushButton {
    background-color: #002200;
    border: 2px solid #00FF00;
    padding: 8px;
    border-radius: 5px;
    font-size: 16px;
}
QPushButton:hover {
    background-color: #00FF00;
    color: #000000;
}
'''

class PropertiesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Свойства операций')
        self.resize(700, 600)
        self.setStyleSheet(MATRIX_STYLE)
        
        layout = QVBoxLayout(self)
        text_browser = QTextBrowser()
        text_browser.setFont(QFont('Courier New', 12))
        
        all_props = f"{properties.PROPERTIES_ADD_SCALAR}\n\n" \
                    f"{properties.PROPERTIES_MULTIPLICATION}\n\n" \
                    f"{properties.PROPERTIES_INVERSE}"
        text_browser.setText(all_props)
        layout.addWidget(text_browser)

class MatrixCalculatorQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Матричный калькулятор (PyQt6)')
        self.resize(1000, 800)
        self.setStyleSheet(MATRIX_STYLE)

        self.init_ui()
        self.update_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # ВЕРХНЯЯ ПАНЕЛЬ
        top_layout = QHBoxLayout()
        
        top_layout.addWidget(QLabel('Операция:'))
        self.op_menu = QComboBox()
        self.op_menu.addItems([
            'Сложение', 'Умножение матриц', 'Умножение на число', 
            'Транспонирование', 'Обратная матрица', 'Определитель',
            'Единичная матрица', 'Нулевая матрица', 'Главная диагональ'
        ])
        self.op_menu.currentIndexChanged.connect(self.update_ui)
        top_layout.addWidget(self.op_menu)

        top_layout.addWidget(QLabel('Размер (NxN):'))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 5)
        self.size_spin.setValue(3)
        self.size_spin.valueChanged.connect(self.update_ui)
        top_layout.addWidget(self.size_spin)
        
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        # ЦЕНТРАЛЬНАЯ ПАНЕЛЬ (МАТРИЦЫ)
        matrix_layout = QHBoxLayout()
        matrix_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Матрица А
        self.frame_A = QVBoxLayout()
        self.frame_A.addWidget(QLabel('Матрица A:'), alignment=Qt.AlignmentFlag.AlignCenter)
        self.table_A = QTableWidget()
        self.setup_table(self.table_A)
        self.frame_A.addWidget(self.table_A)
        matrix_layout.addLayout(self.frame_A)

        # Матрица B (по умолчанию скрыта)
        self.frame_B = QVBoxLayout()
        self.frame_B.addWidget(QLabel('Матрица B:'), alignment=Qt.AlignmentFlag.AlignCenter)
        self.table_B = QTableWidget()
        self.setup_table(self.table_B)
        self.frame_B.addWidget(self.table_B)
        
        self.widget_B = QWidget()
        self.widget_B.setLayout(self.frame_B)
        matrix_layout.addWidget(self.widget_B)

        # Поле для скалярного числа (по умолчанию скрыто)
        self.scalar_layout = QVBoxLayout()
        self.scalar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scalar_layout.addWidget(QLabel('Число (k):'), alignment=Qt.AlignmentFlag.AlignCenter)
        self.scalar_input = QTextEdit()
        self.scalar_input.setFixedSize(120, 40)
        self.scalar_layout.addWidget(self.scalar_input)
        
        self.widget_scalar = QWidget()
        self.widget_scalar.setLayout(self.scalar_layout)
        matrix_layout.addWidget(self.widget_scalar)

        main_layout.addLayout(matrix_layout)
        main_layout.addStretch()

        # НИЖНЯЯ ПАНЕЛЬ (КНОПКИ И РЕЗУЛЬТАТ)
        btn_layout = QHBoxLayout()
        
        self.btn_calc = QPushButton('ВЫЧИСЛИТЬ')
        self.btn_calc.clicked.connect(self.calculate)
        self.btn_props = QPushButton('ПОКАЗАТЬ СВОЙСТВА')
        self.btn_props.clicked.connect(self.show_properties)
        self.btn_clear = QPushButton('ОЧИСТИТЬ')
        self.btn_clear.clicked.connect(self.update_ui)

        btn_layout.addWidget(self.btn_calc)
        btn_layout.addWidget(self.btn_props)
        btn_layout.addWidget(self.btn_clear)
        main_layout.addLayout(btn_layout)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('Courier New', 16))
        self.result_text.setMaximumHeight(250)
        main_layout.addWidget(self.result_text)

    def setup_table(self, table):
        # Настройка внешнего вида таблицы
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setMinimumSize(300, 300)

    def update_ui(self):
        op = self.op_menu.currentText()
        size = self.size_spin.value()
        
        self.result_text.clear()
        
        self.widget_B.setVisible(False)
        self.widget_scalar.setVisible(False)
        self.table_A.setVisible(True)

        # Настройка таблиц
        for table in [self.table_A, self.table_B]:
            table.setRowCount(size)
            table.setColumnCount(size)
            for i in range(size):
                for j in range(size):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont('Courier New', 14, QFont.Weight.Bold)
                    item.setFont(font)
                    table.setItem(i, j, item)

        if op in ['Сложение', 'Умножение матриц']:
            self.widget_B.setVisible(True)
        elif op == 'Умножение на число':
            self.widget_scalar.setVisible(True)
            self.scalar_input.clear()
        elif op in ['Единичная матрица', 'Нулевая матрица']:
            self.table_A.setVisible(False)
            self.result_text.setText(f"Нажмите 'ВЫЧИСЛИТЬ', чтобы сгенерировать матрицу {size}x{size}")

    def get_matrix_from_table(self, table):
        rows = table.rowCount()
        cols = table.columnCount()
        raw_data = []
        
        for i in range(rows):
            row_data = []
            for j in range(cols):
                item = table.item(i, j)
                text = item.text() if item else ''
                row_data.append(text)
            raw_data.append(row_data)
            
        return validators.parse_matrix(raw_data)

    def format_matrix(self, matrix):
        lines = []
        for row in matrix:
            row_str = '  '.join(f"{val:8.2f}" for val in row)
            lines.append(f"[ {row_str} ]")
        return "\n".join(lines)

    def calculate(self):
        op = self.op_menu.currentText()
        size = self.size_spin.value()
        self.result_text.clear()

        try:
            if op in ['Единичная матрица', 'Нулевая матрица']:
                res = matrix_operations.get_identity(size) if op == 'Единичная матрица' else matrix_operations.get_zero(size, size)
                self.result_text.setText(self.format_matrix(res))
                return

            A = self.get_matrix_from_table(self.table_A)

            if op == 'Сложение':
                B = self.get_matrix_from_table(self.table_B)
                validators.check_same_size(A, B)
                res = matrix_operations.add_matrices(A, B)
                
            elif op == 'Умножение матриц':
                B = self.get_matrix_from_table(self.table_B)
                validators.check_multiplication(A, B)
                res = matrix_operations.multiply_matrices(A, B)
                
            elif op == 'Умножение на число':
                scalar = validators.check_scalar(self.scalar_input.toPlainText())
                res = matrix_operations.multiply_by_scalar(A, scalar)
                
            elif op == 'Транспонирование':
                res = matrix_operations.transpose(A)
                
            elif op == 'Обратная матрица':
                validators.check_square(A)
                res = matrix_operations.inverse_matrix(A)
                
            elif op == 'Определитель':
                validators.check_square(A)
                det = matrix_operations.get_determinant(A)
                self.result_text.setText(f"Определитель матрицы A:\ndet(A) = {det:.4f}")
                return
                
            elif op == 'Главная диагональ':
                validators.check_square(A)
                diag = matrix_operations.get_main_diagonal(A)
                self.result_text.setText(f"Элементы главной диагонали:\n{diag}")
                return

            self.result_text.setText("Результат:\n" + self.format_matrix(res))

        except validators.MatrixError as e:
            QMessageBox.critical(self, 'Ошибка валидации', str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Неизвестная ошибка', f"Что-то пошло не так:\n{str(e)}")

    def show_properties(self):
        dialog = PropertiesDialog(self)
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixCalculatorQt()
    window.show()
    sys.exit(app.exec())
