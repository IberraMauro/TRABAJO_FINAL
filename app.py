from flask import Flask, render_template, request, redirect, url_for
import base_de_datos
import modelos

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Instanciamos el Carrito de compras global en la memoria del servidor
# Esto mantendrá los productos seleccionados mientras el servidor esté corriendo
carrito_actual = modelos.Carrito()


# --- RUTA 1: EL CATÁLOGO PRINCIPAL ---
@app.route('/')
def inicio():
    """Busca los productos en SQLite y los muestra en la pantalla principal."""
    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()

    # Traemos todos los productos tecnológicos de la tabla
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
    todos_los_productos = cursor.fetchall()

    conexion.close()

    # Renderizamos index.html pasándole la lista de productos que trajimos
    return render_template('index.html', productos=todos_los_productos)


# --- RUTA 2: ACCIÓN DE AGREGAR AL CARRITO ---
@app.route('/agregar/<int:id_producto>', methods=['POST'])
def agregar_al_carrito(id_producto):
    """Procesa el formulario de compra, usa la POO y actualiza la base de datos."""
    # Obtenemos la cantidad que el usuario escribió en la cajita de texto del HTML
    cantidad = int(request.form.get('cantidad', 1))

    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()

    # 1. Buscamos el producto seleccionado en la base de datos para recrear el Objeto
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos WHERE id_producto = ?", (id_producto,))
    datos_prod = cursor.fetchone()

    if datos_prod:
        # Recreamos el objeto de la clase Producto usando la POO de modelos.py
        producto_objeto = modelos.Producto(
            id_producto=datos_prod[0],
            nombre=datos_prod[1],
            categoria=datos_prod[2],
            precio=datos_prod[3],
            stock=datos_prod[4]
        )

        try:
            # 2. Usamos el método de negocio de nuestra clase Carrito (agrega y descuenta stock en memoria)
            carrito_actual.agregar_item(id_item=id_producto, producto=producto_objeto, cantidad=cantidad)

            # 3. Impactamos el nuevo stock en la base de datos SQLite para que sea permanente
            cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (producto_objeto.stock, id_producto))
            conexion.commit()
            print(f"¡Éxito! Agregado {producto_objeto.nombre} al carrito. Nuevo stock: {producto_objeto.stock}")

        except ValueError as e:
            # Si el método de modelos.py lanza un error por falta de stock, lo atrapamos acá
            print(f"Error al agregar: {e}")

    conexion.close()

    # Una vez hecha la acción, redirigimos al usuario de vuelta al catálogo
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
    """Elimina un ítem del carrito y devuelve el stock correspondiente a SQLite."""
    conexion = base_de_datos.obtener_conexion()
    cursor = conexion.cursor()

    # Buscamos cuántas unidades había en el carrito antes de borrarlo para devolverlas al stock
    cantidad_a_devolver = 0
    for item in carrito_actual.lista_items:
        if item.id_item == id_producto:
            cantidad_a_devolver = item.cantidad
            break

    if cantidad_a_devolver > 0:
        # 1. Ejecutamos el método de nuestra clase Carrito para sacarlo de la lista en memoria
        carrito_actual.quitar_item(id_producto)

        # 2. Leemos el stock actual en la base de datos para sumarle lo devuelto
        cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (id_producto,))
        stock_actual = cursor.fetchone()[0]
        nuevo_stock = stock_actual + cantidad_a_devolver

        # 3. Guardamos el stock actualizado en SQLite
        cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
        conexion.commit()
        print(f"¡Éxito! Ítem quitado. Se devolvieron {cantidad_a_devolver} unidades al stock.")

    conexion.close()

    # Redirigimos de vuelta a la pantalla del carrito para mostrar los cambios
    return redirect(url_for('ver_carrito'))



# --- EJECUCIÓN ---
if __name__ == '__main__':
    app.run(debug=True)
