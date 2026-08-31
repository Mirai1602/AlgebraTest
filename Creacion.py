import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem
)

class CalculadoraMatrices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Matrices")
        self.resize(500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 1. Controles para ingresar Filas y Columnas
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Filas:"))
        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(3)
        control_layout.addWidget(self.spin_filas)

        control_layout.addWidget(QLabel("Columnas:"))
        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(3)
        control_layout.addWidget(self.spin_columnas)

        btn_generar = QPushButton("Generar Matriz")
        btn_generar.clicked.connect(self.generar_matriz)
        control_layout.addWidget(btn_generar)

        layout.addLayout(control_layout)

        # 2. Tabla gráfica para mostrar/ingresar la matriz
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # 3. Botón para leer los datos ingresados
        btn_obtener = QPushButton("Obtener Datos de la Matriz")
        btn_obtener.clicked.connect(self.obtener_matriz)
        layout.addWidget(btn_obtener)

        self.lbl_resultado = QLabel("Matriz creada: ")
        layout.addWidget(self.lbl_resultado)

        self.setLayout(layout)
        self.generar_matriz()

    def generar_matriz(self):
        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()
        self.tabla.setRowCount(filas)
        self.tabla.setColumnCount(columnas)

    def obtener_matriz(self):
        filas = self.tabla.rowCount()
        columnas = self.tabla.columnCount()
        matriz = []

        for f in range(filas):
            fila = []
            for c in range(columnas):
                item = self.tabla.item(f, c)
                valor = int(item.text()) if item and item.text().isdigit() else 0
                fila.append(valor)
            matriz.append(fila)

        self.lbl_resultado.setText(f"Matriz obtenida: {matriz}")
        print("Matriz ingresada en la interfaz:", matriz)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraMatrices()
    ventana.show()
    sys.exit(app.exec())