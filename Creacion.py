import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class CalculadoraMatrices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Matrices - Álgebra Lineal")
        self.resize(800, 550)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        # 1. Controles para definir dimensiones
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Filas:"))
        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(2)
        control_layout.addWidget(self.spin_filas)

        control_layout.addWidget(QLabel("Columnas:"))
        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(2)
        control_layout.addWidget(self.spin_columnas)

        btn_generar = QPushButton("Generar Tablas")
        btn_generar.clicked.connect(self.generar_tablas)
        control_layout.addWidget(btn_generar)

        # BOTÓN: Limpiar todo el contenido de las tablas
        btn_limpiar = QPushButton("🧹 Limpiar Tablas")
        btn_limpiar.clicked.connect(self.limpiar_tablas)
        control_layout.addWidget(btn_limpiar)

        layout_principal.addLayout(control_layout)

        # 2. Contenedor horizontal para Matriz A y Matriz B
        tablas_layout = QHBoxLayout()
        
        # Matriz A
        layout_a = QVBoxLayout()
        layout_a.addWidget(QLabel("<b>Matriz A</b> (Coeficientes)"))
        self.tabla_a = QTableWidget()
        layout_a.addWidget(self.tabla_a)
        tablas_layout.addLayout(layout_a)

        # Matriz B
        layout_b = QVBoxLayout()
        layout_b.addWidget(QLabel("<b>Matriz B</b> (Vector b)"))
        self.tabla_b = QTableWidget()
        layout_b.addWidget(self.tabla_b)
        tablas_layout.addLayout(layout_b)

        layout_principal.addLayout(tablas_layout)

        # 3. Botones de Operaciones
        ops_layout = QHBoxLayout()
        
        btn_suma = QPushButton("Suma (A + B)")
        btn_suma.clicked.connect(lambda: self.operar("+"))
        ops_layout.addWidget(btn_suma)

        btn_resta = QPushButton("Resta (A - B)")
        btn_resta.clicked.connect(lambda: self.operar("-"))
        ops_layout.addWidget(btn_resta)

        btn_mult = QPushButton("Multiplicación (A × B)")
        btn_mult.clicked.connect(lambda: self.operar("*"))
        ops_layout.addWidget(btn_mult)

        # BOTÓN NUEVO: Resolver por Método de Gauss
        btn_gauss = QPushButton("Resolver por Gauss (Ax = B)")
        btn_gauss.clicked.connect(self.ejecutar_gauss)
        ops_layout.addWidget(btn_gauss)

        layout_principal.addLayout(ops_layout)

        # 4. Tabla de Resultado
        layout_principal.addWidget(QLabel("<b>Resultado:</b>"))
        self.tabla_res = QTableWidget()
        layout_principal.addWidget(self.tabla_res)

        self.setLayout(layout_principal)
        self.generar_tablas()

    def generar_tablas(self):
        f = self.spin_filas.value()
        c = self.spin_columnas.value()
        
        for tabla in [self.tabla_a, self.tabla_b]:
            tabla.setRowCount(f)
            tabla.setColumnCount(c)

    def limpiar_tablas(self):
        for tabla in [self.tabla_a, self.tabla_b, self.tabla_res]:
            tabla.clearContents()

    def leer_matriz(self, tabla):
        filas = tabla.rowCount()
        columnas = tabla.columnCount()
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                item = tabla.item(i, j)
                val = float(item.text()) if item and item.text().strip() != "" else 0.0
                fila.append(val)
            matriz.append(fila)
        return matriz

    def mostrar_resultado(self, matriz_res):
        filas = len(matriz_res)
        columnas = len(matriz_res[0])
        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)
        
        for i in range(filas):
            for j in range(columnas):
                val = str(round(matriz_res[i][j], 2))
                self.tabla_res.setItem(i, j, QTableWidgetItem(val))

    # --- MÉTODO DE GAUSS (CÓDIGO NATIVO) ---
    def gauss_resolver(self, matriz_coeficientes, vector_b):
        n = len(matriz_coeficientes)

        # 1. Construir la matriz aumentada [A | b] tomando la primera columna de B
        A = []
        for i in range(n):
            fila = [float(val) for val in matriz_coeficientes[i]]
            fila.append(float(vector_b[i][0]))
            A.append(fila)

        # 2. Eliminación hacia adelante (Triangulación superior)
        for i in range(n):
            # Pivoteo parcial para evitar divisiones por cero
            max_fila = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_fila][i]):
                    max_fila = k
            A[i], A[max_fila] = A[max_fila], A[i]

            pivote = A[i][i]
            if abs(pivote) < 1e-10:
                return None, "El sistema no tiene solución única (pivote igual a cero)."

            # Reducir las filas por debajo del pivote
            for k in range(i + 1, n):
                factor = A[k][i] / pivote
                for j in range(i, n + 1):
                    A[k][j] -= factor * A[i][j]

        # 3. Sustitución hacia atrás
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            suma = A[i][n]
            for j in range(i + 1, n):
                suma -= A[i][j] * x[j]
            x[i] = suma / A[i][i]

        # Retornar como matriz columna (n x 1)
        resultado = [[val] for val in x]
        return resultado, None

    def ejecutar_gauss(self):
        try:
            A = self.leer_matriz(self.tabla_a)
            B = self.leer_matriz(self.tabla_b)

            # Para un sistema Ax = b, A debe ser cuadrada
            if len(A) != len(A[0]):
                QMessageBox.warning(self, "Error", "La Matriz A debe ser cuadrada (mismo número de filas y columnas) para aplicar Gauss.")
                return

            res, error = self.gauss_resolver(A, B)

            if error:
                QMessageBox.warning(self, "Error de Gauss", error)
            else:
                self.mostrar_resultado(res)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error en el cálculo: {e}")

    def operar(self, operacion):
        try:
            A = self.leer_matriz(self.tabla_a)
            B = self.leer_matriz(self.tabla_b)

            filas_A, cols_A = len(A), len(A[0])
            filas_B, cols_B = len(B), len(B[0])

            if operacion in ["+", "-"]:
                if filas_A != filas_B or cols_A != cols_B:
                    QMessageBox.warning(self, "Error", "Las matrices deben tener las mismas dimensiones.")
                    return
                
                res = []
                for i in range(filas_A):
                    fila = []
                    for j in range(cols_A):
                        if operacion == "+":
                            fila.append(A[i][j] + B[i][j])
                        else:
                            fila.append(A[i][j] - B[i][j])
                    res.append(fila)

            elif operacion == "*":
                if cols_A != filas_B:
                    QMessageBox.warning(self, "Error", "Las columnas de A deben ser iguales a las filas de B.")
                    return

                res = []
                for i in range(filas_A):
                    fila = []
                    for j in range(cols_B):
                        suma = 0
                        for k in range(cols_A):
                            suma += A[i][k] * B[k][j]
                        fila.append(suma)
                    res.append(fila)

            self.mostrar_resultado(res)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error en el cálculo: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraMatrices()
    ventana.show()
    sys.exit(app.exec())