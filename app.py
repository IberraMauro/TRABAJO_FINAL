from flask import Flask, render_template, request, redirect, url_for, flash
from catalogo import Catalogo
import modelos


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tienda-tech-flash'

carrito_actual = modelos.Carrito()
catalogo = Catalogo()


@app.context_processor
def inyectar_datos_carrito():
    """Expone datos del carrito a todas las plantillas."""
    return {
        'cantidad_items_carrito': carrito_actual.calcular_cantidad_total_items()
    }


# --- RUTA 1: CATALOGO PRINCIPAL ---
@app.route('/')
def inicio():
    """Busca los productos, calcula el stock virtual y los muestra."""
    productos_para_mostrar = catalogo.listar_productos_con_stock_virtual(carrito_actual)
    return render_template('index.html', productos=productos_para_mostrar)


# --- RUTA 2: ACCION DE AGREGAR AL CARRITO ---
@app.route('/agregar/<int:id_producto>', methods=['POST'])
def agregar_al_carrito(id_producto):
    """Agrega al carrito validando contra el stock virtual disponible."""
    cantidad = int(request.form.get('cantidad', 1))
    producto_agregado = catalogo.agregar_producto_al_carrito(id_producto, cantidad, carrito_actual)

    if producto_agregado:
        flash('Producto agregado al carrito', 'success')

    return redirect(url_for('inicio'))


# --- RUTA 3: VER EL CARRITO ---
@app.route('/carrito')
def ver_carrito():
    """Muestra los items que se agregaron al carrito y calcula los totales."""
    return render_template(
        'carrito.html',
        items=carrito_actual.lista_items,
        total=carrito_actual.calcular_total_general()
    )


# --- RUTA 4: QUITAR UN ITEM DEL CARRITO ---
@app.route('/quitar/<int:id_producto>', methods=['POST'])
def quitar_del_carrito(id_producto):
    """Como nunca descontamos de la base de datos, solo lo borramos de la memoria."""
    carrito_actual.quitar_item(id_producto)
    return redirect(url_for('ver_carrito'))


# --- RUTA 5: FINALIZAR COMPRA ---
@app.route('/comprar', methods=['POST'])
def finalizar_compra():
    """Descuenta todo junto de la base de datos."""
    if len(carrito_actual.lista_items) == 0:
        return redirect(url_for('inicio'))

    catalogo.finalizar_compra(carrito_actual)
    carrito_actual.lista_items.clear()
    flash('¡Compra realizada con éxito!', 'success')
    return redirect(url_for('inicio'))


# --- RUTAS ADMINISTRATIVAS (ABM) ---

@app.route('/admin')
def panel_admin():
    """Muestra el panel ABM con todos los productos."""
    todos_los_productos = catalogo.listar_productos_admin()
    return render_template('admin.html', productos=todos_los_productos)


@app.route('/admin/agregar', methods=['POST'])
def admin_alta():
    """Procesa el formulario para dar de alta un producto nuevo."""
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')
    precio = float(request.form.get('precio', 0))
    stock = int(request.form.get('stock', 0))
    imagen = request.form.get('imagen')

    catalogo.insertar_producto(nombre, categoria, precio, stock, imagen)
    flash('Producto agregado correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/admin/eliminar/<int:id_producto>', methods=['POST'])
def admin_baja(id_producto):
    """Procesa la solicitud de eliminacion de un producto."""
    catalogo.eliminar_producto(id_producto)
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('panel_admin'))


@app.route('/admin/editar/<int:id_producto>', methods=['GET', 'POST'])
def admin_modificacion(id_producto):
    """Muestra el formulario con los datos viejos o procesa el cambio."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        categoria = request.form.get('categoria')
        precio = float(request.form.get('precio', 0))
        stock = int(request.form.get('stock', 0))
        imagen = request.form.get('imagen')

        catalogo.modificar_producto(id_producto, nombre, categoria, precio, stock, imagen)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('panel_admin'))

    prod = catalogo.obtener_producto_por_id(id_producto)
    return render_template('editar.html', producto=prod)


if __name__ == '__main__':
    app.run(debug=True)
