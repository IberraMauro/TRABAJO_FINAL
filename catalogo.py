import base_de_datos
import modelos


class Catalogo:
    """Centraliza la logica de negocio relacionada con productos."""

    def __init__(self, proveedor_conexion=base_de_datos.obtener_conexion) -> None:
        self.proveedor_conexion = proveedor_conexion

    def listar_productos(self):
        """Obtiene todos los productos con los campos usados por el catalogo publico."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock, imagen FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos

    def listar_productos_con_stock_virtual(self, carrito):
        """Devuelve productos con stock disponible descontando lo reservado en el carrito."""
        productos_para_mostrar = []

        for producto in self.listar_productos():
            id_producto = producto[0]
            stock_real = producto[4]
            cantidad_reservada = carrito.obtener_cantidad_producto(id_producto)
            stock_virtual = stock_real - cantidad_reservada

            producto_modificado = (
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                stock_virtual,
                producto[5],
            )
            productos_para_mostrar.append(producto_modificado)

        return productos_para_mostrar

    def obtener_producto_por_id(self, id_producto: int):
        """Obtiene un producto desde la base de datos por su identificador."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_producto, nombre, categoria, precio, stock, imagen FROM productos WHERE id_producto = ?",
            (id_producto,),
        )
        producto = cursor.fetchone()
        conexion.close()
        return producto

    def crear_producto_desde_fila(self, datos_producto):
        """Convierte una fila de la base de datos en un objeto Producto."""
        if not datos_producto:
            return None

        return modelos.Producto(
            id_producto=datos_producto[0],
            nombre=datos_producto[1],
            categoria=datos_producto[2],
            precio=datos_producto[3],
            stock=datos_producto[4],
            imagen=datos_producto[5],
        )

    def agregar_producto_al_carrito(self, id_producto: int, cantidad: int, carrito) -> bool:
        """Agrega un producto al carrito validando el stock virtual disponible."""
        datos_producto = self.obtener_producto_por_id(id_producto)
        producto = self.crear_producto_desde_fila(datos_producto)

        if producto:
            cantidad_reservada = carrito.obtener_cantidad_producto(id_producto)
            stock_disponible_para_agregar = producto.stock - cantidad_reservada

            if cantidad > stock_disponible_para_agregar:
                print(f"Error: Solo quedan {stock_disponible_para_agregar} unidades disponibles.")
            else:
                try:
                    carrito.agregar_item(
                        id_item=id_producto,
                        producto=producto,
                        cantidad=cantidad,
                    )
                    return True
                except ValueError as e:
                    print(f"Error al agregar: {e}")

        return False

    def finalizar_compra(self, carrito) -> None:
        """Descuenta definitivamente el stock de los productos incluidos en el carrito."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()

        for item in carrito.lista_items:
            cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (item.id_item,))
            stock_actual = cursor.fetchone()[0]
            nuevo_stock = stock_actual - item.cantidad
            cursor.execute(
                "UPDATE productos SET stock = ? WHERE id_producto = ?",
                (nuevo_stock, item.id_item),
            )

        conexion.commit()
        conexion.close()

    def listar_productos_admin(self):
        """Obtiene los productos con los campos usados por el panel administrativo."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos

    def insertar_producto(self, nombre: str, categoria: str, precio: float, stock: int, imagen: str) -> None:
        """Alta: guarda un nuevo producto en la base de datos."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO productos (nombre, categoria, precio, stock, imagen)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, categoria, precio, stock, imagen),
        )
        conexion.commit()
        conexion.close()

    def eliminar_producto(self, id_producto: int) -> None:
        """Baja: elimina un producto de la base de datos."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        conexion.commit()
        conexion.close()

    def modificar_producto(
        self,
        id_producto: int,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        imagen: str,
    ) -> None:
        """Modificacion: actualiza los campos editables de un producto."""
        conexion = self.proveedor_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE productos
            SET nombre = ?, categoria = ?, precio = ?, stock = ?, imagen = ?
            WHERE id_producto = ?
            """,
            (nombre, categoria, precio, stock, imagen, id_producto),
        )
        conexion.commit()
        conexion.close()
