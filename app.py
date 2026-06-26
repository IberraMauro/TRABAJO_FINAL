from flask import Flask, render_template, request, redirect, url_for
import base_de_datos
import modelos

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Instanciamos el Carrito de compras global en la memoria del servidor
# Esto mantendrá los productos seleccionados mientras el servidor esté corriendo
carrito_actual = modelos.Carrito()


# --- RUTA 1: CATÁLOGO PRINCIPAL ---
@app.route('/')
def inicio():
    """Busca los productos, calcula el stock virtual y los muestra."""
    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock, imagen FROM productos")
    productos_db = cursor.fetchall()
    conexion.close()

    productos_para_mostrar = []
    for prod in productos_db:
        id_prod = prod[0]
        stock_real = prod[4]
        cantidad_reservada = carrito_actual.obtener_cantidad_producto(id_prod)
        stock_virtual = stock_real - cantidad_reservada

        # Armamos la tupla con el stock virtual
        producto_modificado = (prod[0], prod[1], prod[2], prod[3], stock_virtual, prod[5])

        # AHORA AGREGAMOS TODOS, INCLUSO LOS QUE TIENEN 0
        productos_para_mostrar.append(producto_modificado)

    return render_template('index.html', productos=productos_para_mostrar)

# --- RUTA 2: ACCIÓN DE AGREGAR AL CARRITO ---
@app.route('/agregar/<int:id_producto>', methods=['POST'])
def agregar_al_carrito(id_producto):
    """Agrega al carrito validando contra el stock virtual disponible."""
    cantidad = int(request.form.get('cantidad', 1))

    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock, imagen FROM productos WHERE id_producto = ?", (id_producto,))
    datos_prod = cursor.fetchone()
    conexion.close()

    if datos_prod:
        # Recreamos el objeto Producto
        producto_objeto = modelos.Producto(
            id_producto=datos_prod[0], nombre=datos_prod[1], categoria=datos_prod[2],
            precio=datos_prod[3], stock=datos_prod[4], imagen=datos_prod[5]
        )

        # Calculamos cuánto nos queda disponible realmente para agregar
        cantidad_reservada = carrito_actual.obtener_cantidad_producto(id_producto)
        stock_disponible_para_agregar = producto_objeto.stock - cantidad_reservada

        # Validamos
        if cantidad > stock_disponible_para_agregar:
            print(f"Error: Solo quedan {stock_disponible_para_agregar} unidades disponibles.")
        else:
            try:
                # Se agrega exitosamente a la memoria temporal
                carrito_actual.agregar_item(id_item=id_producto, producto=producto_objeto, cantidad=cantidad)
            except ValueError as e:
                print(f"Error al agregar: {e}")

    return redirect(url_for('inicio'))

# --- RUTA 3: VER EL CARRITO ---
@app.route('/carrito')
def ver_carrito():
    """Muestra los ítems que se agregaron al carrito y calcula los totales."""
    # Le pasamos al HTML la lista de ítems y el cálculo del total general usando los métodos de POO
    return render_template(
        'carrito.html',
        items=carrito_actual.lista_items,
        total=carrito_actual.calcular_total_general()
    )



# --- RUTA 4: QUITAR UN ÍTEM DEL CARRITO ---
@app.route('/quitar/<int:id_producto>', methods=['POST'])
def quitar_del_carrito(id_producto):
    """Como nunca descontamos de la base de datos, solo lo borramos de la memoria."""
    carrito_actual.quitar_item(id_producto)
    return redirect(url_for('ver_carrito'))



# --- RUTA 5: FINALIZAR COMPRA ---
@app.route('/comprar', methods=['POST'])
def finalizar_compra():
    """Este es el momento donde descontamos todo junto de la base de datos."""
    if len(carrito_actual.lista_items) == 0:
        return redirect(url_for('inicio'))

    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()

    # Recorremos todo lo que el usuario decidió comprar
    for item in carrito_actual.lista_items:
        # Buscamos el stock actual en SQLite
        cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (item.id_item,))
        stock_actual = cursor.fetchone()[0]

        # Descontamos y actualizamos el archivo .db permanentemente
        nuevo_stock = stock_actual - item.cantidad
        cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, item.id_item))

    conexion.commit()
    conexion.close()

    # Vaciamos el carrito de la memoria porque la compra ya se efectuó
    carrito_actual.lista_items.clear()

    # Redirigimos al inicio
    return redirect(url_for('inicio'))

# --- RUTAS ADMINISTRATIVAS (ABM) ---

@app.route('/admin')
def panel_admin():
    """Muestra el panel ABM con todos los productos."""
    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
    todos_los_productos = cursor.fetchall()
    conexion.close()
    return render_template('admin.html', productos=todos_los_productos)

@app.route('/admin/agregar', methods=['POST'])
def admin_alta():
    """Procesa el formulario para dar de alta un producto nuevo."""
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')
    precio = float(request.form.get('precio', 0))
    stock = int(request.form.get('stock', 0))
    imagen = request.form.get('imagen')

    # Llamamos a nuestra función de base_de_datos.py
    base_de_datos.insertar_producto_nuevo(nombre, categoria, precio, stock, imagen)
    return redirect(url_for('panel_admin'))

@app.route('/admin/eliminar/<int:id_producto>', methods=['POST'])
def admin_baja(id_producto):
    """Procesa la solicitud de eliminación (Baja) de un producto."""
    base_de_datos.eliminar_producto_por_id(id_producto)
    return redirect(url_for('panel_admin'))

@app.route('/admin/editar/<int:id_producto>', methods=['GET', 'POST'])
def admin_modificacion(id_producto):
    """Muestra el formulario con los datos viejos (GET) o procesa el cambio (POST)."""
    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        # Si el usuario envió el formulario con los datos modificados
        nombre = request.form.get('nombre')
        categoria = request.form.get('categoria')
        precio = float(request.form.get('precio', 0))
        stock = int(request.form.get('stock', 0))
        imagen = request.form.get('imagen')

        base_de_datos.modificar_producto_existente(id_producto, nombre, categoria, precio, stock, imagen)
        conexion.close()
        return redirect(url_for('panel_admin'))

    else:
        # Si el usuario solo hizo clic en "Editar", buscamos sus datos para mostrarlos en las cajas
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock, imagen FROM productos WHERE id_producto = ?", (id_producto,))
        prod = cursor.fetchone()
        conexion.close()
        return render_template('editar.html', producto=prod)


# --- EJECUCIÓN ---
if __name__ == '__main__':
    app.run(debug=True)



