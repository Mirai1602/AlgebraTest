import sys
from fractions import Fraction

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, 
    QMessageBox, QScrollArea, QTextEdit
)
from PyQt6.QtCore import Qt


class MatrizModel:

    # Suma
    @staticmethod
    def sumar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]
        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] += m[i][j]
        return res

    # Resta
    @staticmethod
    def restar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]
        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] -= m[i][j]
        return res

    # Multiplicación
    @staticmethod
    def multiplicar(matrices):
        res = matrices[0]
        for m in matrices[1:]:
            f_A, c_A = len(res), len(res[0])
            f_B, c_B = len(m), len(m[0])
            sub_res = []
            for i in range(f_A):
                fila = []
                for j in range(c_B):
                    suma = 0
                    for k in range(c_A):
                        suma += res[i][k] * m[k][j]
                    fila.append(suma)
                sub_res.append(fila)
            res = sub_res
        return res

    # Formato de matriz
    @staticmethod
    def formato_matriz_str(matriz, titulo=""):
        texto = f"--- {titulo} ---\n" if titulo else ""

        for fila in matriz:

            # Si el valor es una fracción, mostrarla como fracción
            if any(isinstance(val, Fraction) for val in fila):
                valores = []

                for val in fila:
                    if isinstance(val, Fraction):
                        if val.denominator == 1:
                            valores.append(str(val.numerator))
                        else:
                            valores.append(
                                f"{val.numerator}/{val.denominator}"
                            )
                    else:
                        valores.append(f"{val:.2f}")

                coefs = "  ".join(
                    [f"{val:>8}" for val in valores[:-1]]
                )
                b_val = f"{valores[-1]:>8}"

                texto += f"[ {coefs}  | {b_val} ]\n"

            else:
                coefs = "  ".join([f"{val:8.2f}" for val in fila[:-1]])
                b_val = f"{fila[-1]:8.2f}"
                texto += f"[ {coefs}  | {b_val} ]\n"

        return texto + "\n"

    # Gauss
    @staticmethod
    def gauss_resolver_completo(A_orig, b_orig):
        m = len(A_orig)        # Número de ecuaciones
        n = len(A_orig[0])     # Número de variables
        
        Ab = []
        for i in range(m):
            fila = [Fraction(str(val)) for val in A_orig[i]]
            fila.append(Fraction(str(b_orig[i][0])))
            Ab.append(fila)

        pasos_txt = MatrizModel.formato_matriz_str(
            Ab, "Matriz Aumentada Inicial (Ab)"
        )
        
        fila_pivote = 0

        for col in range(n):
            if fila_pivote >= m:
                break

            max_i = fila_pivote
            for i in range(fila_pivote + 1, m):
                if abs(Ab[i][col]) > abs(Ab[max_i][col]):
                    max_i = i

            if Ab[max_i][col] == 0:
                pasos_txt += f"Columna {col + 1}: Sin pivote válido.\n\n"
                continue

            if max_i != fila_pivote:
                Ab[fila_pivote], Ab[max_i] = Ab[max_i], Ab[fila_pivote]
                pasos_txt += f"Paso: Intercambio de Fila {fila_pivote + 1} con Fila {max_i + 1}\n"
                pasos_txt += MatrizModel.formato_matriz_str(Ab)

            pivote = Ab[fila_pivote][col]

            for i in range(fila_pivote + 1, m):
                factor = Ab[i][col] / pivote

                if factor != 0:
                    for j in range(col, n + 1):
                        Ab[i][j] -= factor * Ab[fila_pivote][j]

                    if factor.denominator == 1:
                        factor_txt = str(factor.numerator)
                    else:
                        factor_txt = f"{factor.numerator}/{factor.denominator}"

                    pasos_txt += (
                        f"Paso: Fila {i + 1} = Fila {i + 1} - "
                        f"({factor_txt}) * Fila {fila_pivote + 1}\n"
                    )
                    pasos_txt += MatrizModel.formato_matriz_str(Ab)

            fila_pivote += 1

        rango_A = 0
        rango_Ab = 0

        for i in range(m):
            coefs_ceros = all(Ab[i][j] == 0 for j in range(n))
            indep_cero = Ab[i][n] == 0

            if not coefs_ceros:
                rango_A += 1
                rango_Ab += 1
            elif not indep_cero:
                rango_Ab += 1

        clasificacion = ""
        solucion = None
        verificacion_txt = ""

        if rango_A < rango_Ab:
            clasificacion = "Sistema Inconsistente: Sin Solución (Incompatible)."
            solucion = "SIN SOLUCIÓN (Sistema Incompatible)"

        elif rango_A < n:
            clasificacion = "Sistema Consistente Indeterminado: Infinitas Soluciones."
            solucion = "INFINITAS SOLUCIONES (Sistema Indeterminado)"

        else:
            clasificacion = "Sistema Consistente Determinado: Presenta Solución Única."

            x = [Fraction(0) for _ in range(n)]

            for i in range(n - 1, -1, -1):
                suma = Ab[i][n]

                for j in range(i + 1, n):
                    suma -= Ab[i][j] * x[j]

                x[i] = suma / Ab[i][i]

            solucion = [[val] for val in x]

            verificacion_txt = "=== VERIFICACIÓN AUTOMÁTICA (Ax = b) ===\n"

            for i in range(m):
                calculado = sum(
                    Fraction(str(A_orig[i][j])) * x[j]
                    for j in range(n)
                )

                esperado = Fraction(str(b_orig[i][0]))

                calculado_txt = (
                    f"{calculado.numerator}/{calculado.denominator}"
                    if calculado.denominator != 1
                    else str(calculado.numerator)
                )

                esperado_txt = (
                    f"{esperado.numerator}/{esperado.denominator}"
                    if esperado.denominator != 1
                    else str(esperado.numerator)
                )

                verificacion_txt += (
                    f"Ecuación {i + 1}: {calculado_txt} = {esperado_txt} "
                    f"-> {'OK' if calculado == esperado else 'ERROR'}\n"
                )

        return pasos_txt, clasificacion, solucion, verificacion_txt

    # Gauss-Jordan
    @staticmethod
    def metodo_gauss_jordan(A_orig, b_orig):
        m = len(A_orig)        # Número de ecuaciones
        n = len(A_orig[0])     # Número de variables

        # Construir matriz aumentada
        Ab = []
        for i in range(m):
            fila = [Fraction(str(val)) for val in A_orig[i]]
            fila.append(Fraction(str(b_orig[i][0])))
            Ab.append(fila)

        pasos_txt = MatrizModel.formato_matriz_str(
            Ab, "Matriz Aumentada Inicial (Ab)"
        )

        for k in range(min(m, n)):
            pivote = Ab[k][k]

            # Si el pivote es 0, buscar otra fila para intercambiar
            if pivote == 0:
                for r in range(k + 1, m):
                    if Ab[r][k] != 0:
                        Ab[k], Ab[r] = Ab[r], Ab[k]
                        pivote = Ab[k][k]
                        pasos_txt += f"Paso: Intercambio Fila {k + 1} con Fila {r + 1}\n"
                        pasos_txt += MatrizModel.formato_matriz_str(Ab)
                        break

            # Si el pivote sigue siendo 0, el sistema no es determinado
            if pivote == 0:
                pasos_txt += f"\nColumna {k + 1}: No se encontró un pivote válido.\n"
                return (
                    pasos_txt,
                    "Sistema Inconsistente o Indeterminado",
                    "SIN SOLUCIÓN / INFINITAS SOLUCIONES",
                    ""
                )

            # Normalizar fila pivote (hacer pivote = 1)
            for j in range(n + 1):
                Ab[k][j] /= pivote

            if pivote.denominator == 1:
                pivote_txt = str(pivote.numerator)
            else:
                pivote_txt = f"{pivote.numerator}/{pivote.denominator}"

            pasos_txt += (
                f"Paso: Fila {k + 1} = Fila {k + 1} / "
                f"{pivote_txt} (Convertir pivote en 1)\n"
            )

            pasos_txt += MatrizModel.formato_matriz_str(Ab)

            # Reducir ceros arriba y abajo del pivote
            for i in range(m):
                if i != k:
                    factor = Ab[i][k]

                    if factor != 0:
                        for j in range(n + 1):
                            Ab[i][j] -= factor * Ab[k][j]

                        if factor.denominator == 1:
                            factor_txt = str(factor.numerator)
                        else:
                            factor_txt = (
                                f"{factor.numerator}/"
                                f"{factor.denominator}"
                            )

                        pasos_txt += (
                            f"Paso: Fila {i + 1} = Fila {i + 1} - "
                            f"({factor_txt}) * Fila {k + 1}\n"
                        )

                        pasos_txt += MatrizModel.formato_matriz_str(Ab)

        # Extraer solución
        x = [Ab[i][n] for i in range(m)]
        solucion = [[val] for val in x]
        clasificacion = "Sistema Consistente Determinado: Solución Única"

        # Verificación Ax = b
        verificacion_txt = "=== VERIFICACIÓN AUTOMÁTICA (Ax = b) ===\n"

        for i in range(m):
            calculado = sum(
                Fraction(str(A_orig[i][j])) * x[j]
                for j in range(n)
            )

            esperado = Fraction(str(b_orig[i][0]))

            calculado_txt = (
                f"{calculado.numerator}/{calculado.denominator}"
                if calculado.denominator != 1
                else str(calculado.numerator)
            )

            esperado_txt = (
                f"{esperado.numerator}/{esperado.denominator}"
                if esperado.denominator != 1
                else str(esperado.numerator)
            )

            verificacion_txt += (
                f"Ecuación {i + 1}: {calculado_txt} = {esperado_txt} "
                f"-> {'OK' if calculado == esperado else 'ERROR'}\n"
            )

        return pasos_txt, clasificacion, solucion, verificacion_txt


class CalculadoraMatrices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Álgebra Lineal - UAM")
        self.resize(1000, 750)
        self.tablas = []
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        grupo_filas = QHBoxLayout()
        grupo_filas.setSpacing(6)
        grupo_filas.addWidget(QLabel("<b>Filas (m):</b>"))
        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(3)
        self.spin_filas.setFixedWidth(85)
        grupo_filas.addWidget(self.spin_filas)
        control_layout.addLayout(grupo_filas)

        grupo_cols = QHBoxLayout()
        grupo_cols.setSpacing(6)
        grupo_cols.addWidget(QLabel("<b>Columnas (n):</b>"))
        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(4)
        self.spin_columnas.setFixedWidth(85)
        grupo_cols.addWidget(self.spin_columnas)
        control_layout.addLayout(grupo_cols)

        grupo_tablas = QHBoxLayout()
        grupo_tablas.setSpacing(6)
        grupo_tablas.addWidget(QLabel("<b>N° de Tablas:</b>"))
        self.spin_num_tablas = QSpinBox()
        self.spin_num_tablas.setRange(1, 5)
        self.spin_num_tablas.setValue(1)
        self.spin_num_tablas.setFixedWidth(85)
        grupo_tablas.addWidget(self.spin_num_tablas)
        control_layout.addLayout(grupo_tablas)

        btn_generar = QPushButton("Generar Tablas")
        btn_generar.clicked.connect(self.generar_tablas)
        control_layout.addWidget(btn_generar)

        btn_limpiar = QPushButton("🧹 Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_tablas)
        control_layout.addWidget(btn_limpiar)

        control_layout.addStretch()
        layout_principal.addLayout(control_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.contenedor_tablas = QWidget()
        self.tablas_layout = QHBoxLayout(self.contenedor_tablas)
        self.tablas_layout.setSpacing(20)
        self.scroll_area.setWidget(self.contenedor_tablas)
        layout_principal.addWidget(self.scroll_area)

        ops_layout = QHBoxLayout()
        
        btn_suma = QPushButton("Suma (+)")
        btn_suma.clicked.connect(lambda: self.ejecutar_operacion("+"))
        ops_layout.addWidget(btn_suma)

        btn_resta = QPushButton("Resta (-)")
        btn_resta.clicked.connect(lambda: self.ejecutar_operacion("-"))
        ops_layout.addWidget(btn_resta)

        btn_mult = QPushButton("Multiplicación (*)")
        btn_mult.clicked.connect(lambda: self.ejecutar_operacion("*"))
        ops_layout.addWidget(btn_mult)

        btn_gauss = QPushButton("Resolver Gauss")
        btn_gauss.clicked.connect(self.ejecutar_gauss)
        ops_layout.addWidget(btn_gauss)

        btn_gauss_jordan = QPushButton("Resolver Gauss-Jordan")
        btn_gauss_jordan.clicked.connect(self.ejecutar_gauss_jordan)
        ops_layout.addWidget(btn_gauss_jordan)

        layout_principal.addLayout(ops_layout)

        layout_principal.addWidget(QLabel("<b>Vector Solución (x):</b>"))
        self.tabla_res = QTableWidget()
        self.tabla_res.setMaximumHeight(100)
        layout_principal.addWidget(self.tabla_res)

        layout_principal.addWidget(QLabel("<b>Procedimiento Paso a Paso y Clasificación:</b>"))
        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        layout_principal.addWidget(self.txt_bitacora)

        self.setLayout(layout_principal)
        self.generar_tablas()

    def generar_tablas(self):
        for i in reversed(range(self.tablas_layout.count())):
            widget = self.tablas_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        self.tablas.clear()
        f = self.spin_filas.value()
        c = self.spin_columnas.value()
        num_tablas = self.spin_num_tablas.value()
        letras = ["A (Aumentada/Coefs)", "B (Indep)", "C", "D", "E"]

        for i in range(num_tablas):
            box = QVBoxLayout()
            box.addWidget(QLabel(f"<b>Matriz {letras[i]}</b>"))
            
            tabla = QTableWidget()
            tabla.setRowCount(f)
            tabla.setColumnCount(1 if (num_tablas >= 2 and i == 1) else c)
            box.addWidget(tabla)
            
            w = QWidget()
            w.setLayout(box)
            self.tablas_layout.addWidget(w)
            self.tablas.append(tabla)

    def limpiar_tablas(self):
        for tabla in self.tablas + [self.tabla_res]:
            tabla.clearContents()
        self.txt_bitacora.clear()

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
        self.tabla_res.clear()
        
        # Caso 1: Cadena de texto (Sin solución / Infinitas soluciones)
        if isinstance(matriz_res, str):
            self.tabla_res.setRowCount(1)
            self.tabla_res.setColumnCount(1)
            item = QTableWidgetItem(matriz_res)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_res.setItem(0, 0, item)
            self.tabla_res.setSpan(0, 0, 1, 1)
            return

        # Caso 2: Sin datos o None
        if not matriz_res:
            self.tabla_res.setRowCount(0)
            self.tabla_res.setColumnCount(0)
            return
        
        # Caso 3: Matriz de valores numéricos
        filas = len(matriz_res)
        columnas = len(matriz_res[0])
        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)
        
        for i in range(filas):
            for j in range(columnas):
                val = str(round(matriz_res[i][j], 4))
                self.tabla_res.setItem(i, j, QTableWidgetItem(val))

    def ejecutar_operacion(self, operacion):
        try:
            if len(self.tablas) < 2:
                QMessageBox.warning(self, "Error", "Se necesitan al menos 2 tablas para realizar operaciones aritméticas.")
                return

            matrices = [self.leer_matriz(t) for t in self.tablas]
            f_base, c_base = len(matrices[0]), len(matrices[0][0])

            if operacion in ["+", "-"]:
                for m in matrices[1:]:
                    if len(m) != f_base or len(m[0]) != c_base:
                        QMessageBox.warning(self, "Error", "Las matrices deben tener dimensiones idénticas.")
                        return
                res = MatrizModel.sumar(matrices) if operacion == "+" else MatrizModel.restar(matrices)

            elif operacion == "*":
                for i in range(len(matrices) - 1):
                    if len(matrices[i][0]) != len(matrices[i+1]):
                        QMessageBox.warning(self, "Error", "Dimensiones incompatibles para multiplicar.")
                        return
                res = MatrizModel.multiplicar(matrices)

            self.mostrar_resultado(res)
            self.txt_bitacora.setText(f"Operación {operacion} realizada con éxito.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")

    def obtener_A_y_B(self):
        matriz_A_raw = self.leer_matriz(self.tablas[0])
        num_cols_A = len(matriz_A_raw[0])

        if len(self.tablas) == 1 or num_cols_A > len(matriz_A_raw):
            if num_cols_A < 2:
                QMessageBox.warning(self, "Error", "La tabla debe tener al menos 2 columnas para incluir los coeficientes y el término independiente.")
                return None, None
            A = [fila[:-1] for fila in matriz_A_raw]
            B = [[fila[-1]] for fila in matriz_A_raw]
        else:
            A = matriz_A_raw
            B = self.leer_matriz(self.tablas[1])

            if len(A) != len(B):
                QMessageBox.warning(self, "Error", "La Matriz A y el Vector B deben tener el mismo número de filas.")
                return None, None

        return A, B

    def ejecutar_gauss(self):
        try:
            A, B = self.obtener_A_y_B()
            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = MatrizModel.gauss_resolver_completo(A, B)

            self.mostrar_resultado(solucion)

            reporte = (
                f"======================================\n"
                f"   MÉTODO: GAUSS\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                f"======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )
            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar Gauss: {e}")

    def ejecutar_gauss_jordan(self):
        try:
            A, B = self.obtener_A_y_B()
            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = MatrizModel.metodo_gauss_jordan(A, B)

            self.mostrar_resultado(solucion)

            reporte = (
                f"======================================\n"
                f"   MÉTODO: GAUSS-JORDAN\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                f"======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )
            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar Gauss-Jordan: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraMatrices()
    ventana.show()
    sys.exit(app.exec())