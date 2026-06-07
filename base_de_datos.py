import sqlite3

def obtener_conexion():
    """Crea y devuelve la conexión a la base de datos local."""
    # Esto creará el archivo tienda.db automáticamente si no existe
    return sqlite3.connect("tienda.db")

def crear_tablas():
    """Crea la tabla de productos si aún no existe en el archivo."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Escribimos nuestra instrucción SQL para crear la tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Tabla 'productos' verificada/creada con éxito.")

def insertar_productos_iniciales():
    """Inserta algunos productos tecnológicos de prueba si la tabla está vacía."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificamos si ya hay productos para no duplicarlos
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        productos_prueba = [
            ("Monitor 24 pulgadas", "Monitores", 150000.0, 10),
            ("Teclado Mecánico RGB", "Periféricos", 85000.0, 15),
            ("Mouse Inalámbrico", "Periféricos", 25000.0, 20),
            ("Auriculares Gaming", "Audio", 60000.0, 8)
        ]

        # Insertamos los datos de prueba
        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        ''', productos_prueba)

        conexion.commit()
        print("Productos de prueba insertados en la base de datos.")
    else:
        print("La base de datos ya contiene productos, no se insertaron nuevos.")

    conexion.close()

# --- EJECUCIÓN DIRECTA ---
if __name__ == "__main__":
    print("--- PREPARANDO BASE DE DATOS ---")
    crear_tablas()
    insertar_productos_iniciales()
    print("Base de datos lista")
