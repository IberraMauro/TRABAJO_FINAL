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
            stock INTEGER NOT NULL,
            imagen TEXT NOT NULL
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
            ("Monitor 24 pulgadas", "Monitores", 150000.0, 10, "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500"),
            ("Teclado Mecánico RGB", "Periféricos", 85000.0, 15, "https://http2.mlstatic.com/D_Q_NP_891961-MLA100174230909_122025-O.webp"),
            ("Mouse Inalámbrico", "Periféricos", 25000.0, 20, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500"),
            ("Auriculares Gaming", "Audio", 60000.0, 8, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-XA_Cks2J6V_DE_3N_3Juuk2YBTRfHE62DHNBgozEYRGR4HswPFJGqxps&s=10"),
            ("Silla Gamer Ergonómica FT-055", "Muebles", 250000.0, 5, "https://acdn-us.mitiendanube.com/stores/006/281/009/products/001-1f61129394f297f90317647726844734-1024-1024.webp"),
            ("Micrófono Condensador USB", "Audio", 45000.0, 12, "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=500"),
            ("Placa de Video RTX 4060", "Componentes", 600000.0, 3, "https://static.nb.com.ar/i/nb_PLACA-DE-VIDEO-GIGABYTE-RTX-4060-EAGLE-OC-8GB_ver_1926c9b72f1f01cb8c9b572a79f75e8a.jpg"),
            ("Memoria RAM 16GB DDR4", "Componentes", 55000.0, 25, "https://mauricomputacion.com.ar/images/productos/23853.webp"),
            ("Disco Sólido SSD 1TB", "Almacenamiento", 80000.0, 30, "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=500"),
            ("Gabinete ATX Cristal Templado", "Componentes", 95000.0, 7, "https://www.gamingcity.com.ar/thumb/000000000001717318086Gabinete-ASUS-TUF-Gaming-GT502-Horizon-White-ATX-Vidrio-Templado_800x800.jpg"),
            ("Webcam Full HD 1080p", "Periféricos", 35000.0, 18, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlEA59LOQVUqkOfbc1BkeOrGryiaeBaA0300WfYiOWwVQqZ7Yb3UHJqA&s=10"),
            ("Pad Mouse XXL RGB", "Accesorios", 15000.0, 40, "https://casatecno.com.ar/img/Public/1108/1741-producto-d-nq-np-2x-763046-mlu73342903412-122023-f.jpg"),
            ("Procesador Ryzen 5 5600G", "Componentes", 220000.0, 10, "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500"),
            ("Fuente de Poder 650W 80+", "Componentes", 75000.0, 15, "https://http2.mlstatic.com/D_NQ_NP_640995-MLA99936132579_112025-O.webp"),
            ("Volante Logitech G29 + Pedales", "Accesorios", 469829.0, 26, "https://mexx-img-2019.s3.amazonaws.com/Volante-Logitech-G29-Pedales-Ps4-Ps5-Pc_30260_1.jpeg"),
            ('Tv Led 24" Kanji 60Hz KJ-24MT005-2', "Tv", 125319.0, 39, "https://mexx-img-2019.s3.amazonaws.com/Tv-Led-24-Kanji-60Hz-KJ-24MT005-2_50360_2.jpeg"),
            ("Consola Portatil Anbernic RG353VS TR", "Consolas", 204999.0, 50, "https://mexx-img-2019.s3.amazonaws.com/Consola-Portatil-Anbernic-RG353VS-TR-Negro_50620_1.jpeg"),
            ("Impresora Pantum Láser Mono P2509W", "Impresoras", 138619.0, 23, "https://mexx-img-2019.s3.amazonaws.com/Impresora-Pantum-laser-Mono-P2509W_47605_1.jpeg"),
            ('Notebook Kanji Celeron N4020C 4Gb Ssd 128Gb 15.6" Win11', "Notebooks", 300000.0, 19, "https://mexx-img-2019.s3.amazonaws.com/Notebook-Kanji-Celeron-N4020C-4Gb-Ssd-128Gb-15-Win11_51258_1.jpeg"),
            ("Memoria SD 128 Gb Canvas Go Plus Gen4 Kingston 4k", "Tarjetas de Memoria", 44689.0, 98, "https://mexx-img-2019.s3.amazonaws.com/Memoria-SD-128-Gb-Canvas-Go-Plus-Gen4-Kingston-4K_49898_1.jpeg"),
            ('Monitor Gamer 27" Level Up Curvo Full Hd 200Hz 1Ms 27-UP6580C', "Monitores", 278119.0, 60, "https://mexx-img-2019.s3.amazonaws.com/Monitor-Gamer-27-Level-Up-Curvo-Full-Hd-200Hz-1Ms-27-UP6580C_50090_1.jpeg"),
            ("Impresora Hp Láser Mono M501DN", "Impresoras", 587999.0, 41, "https://mexx-img-2019.s3.amazonaws.com/37679_1.jpeg"),
            ("Parlante Logitech Z407 Graphite Bluetooth", "Audio", 186189.0, 23, "https://mexx-img-2019.s3.amazonaws.com/Parlante-Logitech-Z407-Graphite-Bluetooth_39981_1.jpeg"),
            ("Pen Drive 128 Gb Kingston Exodia DTX Negro", "Pen Drives", 24999.0, 71, "https://mexx-img-2019.s3.amazonaws.com/Pen-Drive-128-Gb-Kingston-Exodia-DTX-Negro_47243_1.jpeg"),
            ("Proyector Epson EpiqVision CO-FH02", "Proyectores", 853289.0, 16, "https://mexx-img-2019.s3.amazonaws.com/47947_1.jpeg"),
            ('Notebook Nsx Alkon Core i5 8Gb Ssd 256Gb 14" Win11', "Notebooks", 565139.0, 34, "https://mexx-img-2019.s3.amazonaws.com/Notebook-Nsx-Alkon-Core-i5-8Gb-Ssd-256Gb-14-Win-11_51000_1.jpeg"),
            ("Adaptador Bluetooth TP-link UB500", "Multimedia", 11420.0, 61, "https://fullh4rd.com.ar/img/productos/30/adaptador-bluetooth-tplink-ub500-plus-long-range-largo-alcance-0.jpg"),
            ("Adaptador coolermaster 3x8 pin PCIE", "Multimedia", 13455.0, 30, "https://fullh4rd.com.ar/img/productos/54/adaptador-coolermaster-90-3x8-pin-pcie-a-12vhpw-pseries-mwegxxg-0.jpg"),
            ("Joystick trust yula pc ps3 GXT540", "Consolas", 41670.0, 26, "https://fullh4rd.com.ar/img/productos/44/joystick-trust-yula-pc-ps3-gxt540-1.jpg"),
            ("Parlante genius SP-HF180 6W", "Audio", 15808.0, 43, "https://fullh4rd.com.ar/img/productos/15/parlante-genius-sphf180-6w-usb-power-madera-0.jpg"),
            ("Camara IP ezviz H9C dual 2k", "Perifericos", 121419.0, 15, "https://fullh4rd.com.ar/img/productos/79/camara-ip-ezviz-h9c-dual-2k-wifi-doble-lente-exterior-0.jpg"),
            ("Router Asus RT-N300 B1", "Perifericos", 26621.0, 9, "https://fullh4rd.com.ar/img/productos/27/router-asus-rtn300-b1-300mbps-5dbi-0.jpg")
        ]

        # Insertamos los datos de prueba
        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, precio, stock, imagen)
            VALUES (?, ?, ?, ?, ?)
        ''', productos_prueba)

        conexion.commit()
        print("Productos de prueba insertados en la base de datos.")
    else:
        print("La base de datos ya contiene productos, no se insertaron nuevos.")

    conexion.close()

def eliminar_producto_por_id(id_producto: int):
    """Baja: Elimina un producto permanentemente de la tabla."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
    conexion.commit()
    conexion.close()

def insertar_producto_nuevo(nombre: str, categoria: str, precio: float, stock: int, imagen: str):
    """Alta: Guarda un nuevo producto tecnológico en la tabla."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, categoria, precio, stock, imagen)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, categoria, precio, stock, imagen))
    conexion.commit()
    conexion.close()

def modificar_producto_existente(id_producto: int, nombre: str, categoria: str, precio: float, stock: int, imagen: str):
    """Modificación: Actualiza todos los campos de un producto específico."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, categoria = ?, precio = ?, stock = ?, imagen = ?
        WHERE id_producto = ?
    ''', (nombre, categoria, precio, stock, imagen, id_producto))
    conexion.commit()
    conexion.close()


# --- EJECUCIÓN DIRECTA ---
if __name__ == "__main__":
    print("--- PREPARANDO BASE DE DATOS ---")
    crear_tablas()
    insertar_productos_iniciales()
    print("Base de datos lista")
