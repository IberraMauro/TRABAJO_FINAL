class Producto:
    #-Representa un artículo tecnológico de la tienda-

    def __init__(self, id_producto: int, nombre: str, categoria: str, precio: float, stock: int, imagen: str = "") ->None:
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

    def hay_stock(self, cantidad_requerida: int) ->bool:
        #-Verifica si hay stock-
        return self.stock >= cantidad_requerida

    def actualizar_stock(self, cantidad: int) ->None:
        #-Modifica el stock-
        self.stock += cantidad


class ItemCarrito:
    #-Representa un producto dentro del carrito de compras-

    def __init__(self, id_item: int, producto: Producto, cantidad: int) ->None:
        #-Extraemos los datos del objeto Producto-
        self.id_item = id_item
        self.nombre_producto = producto.nombre
        self.precio_unitario = producto.precio
        self.categoria = producto.categoria
        self.cantidad = cantidad
        self.imagen = producto.imagen

    def calcular_subtotal(self) ->float:
        #-Devuelve el costo total de esta línea-
        return self.precio_unitario * self.cantidad

    def modificar_cantidad(self, nueva_cantidad: int) ->None:
        #-Actualiza la cantidad validando que sea un número positivo-
        if nueva_cantidad > 0:
            self.cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad debe ser positiva.")


class Carrito:
    def __init__(self) ->None:
        self.lista_items = []

    def agregar_item(self, id_item: int, producto: Producto, cantidad: int) ->None:
        """Agrega un producto al carrito o incrementa la cantidad si ya existe."""
        # 1. Validar que haya suficiente stock disponible en el objeto Producto
        if producto.stock < cantidad:
            raise ValueError(f"No hay suficiente stock disponible para {producto.nombre}.")

        # 2. BUSQUEDA: Verificar si el producto ya está en el carrito
        producto_encontrado = False
        for item in self.lista_items:
            if item.id_item == id_item:
                # Si existe, en vez de duplicarlo, sumamos la nueva cantidad
                item.cantidad += cantidad
                producto_encontrado = True
                break  # Salimos del bucle porque ya lo encontramos

        # 3. Recorrimos toda la lista y NO existía, lo agregamos como ítem nuevo
        if not producto_encontrado:
            nuevo_item = ItemCarrito(
                id_item=id_item,
                producto=producto,
                cantidad=cantidad
            )
            self.lista_items.append(nuevo_item)

        # 4. Descontamos el stock del objeto
        producto.stock -= cantidad

    def quitar_item(self, id_item: int) ->None:
        #-Busca un ítem por su ID y lo elimina de la lista-
        for item in self.lista_items:
            if item.id_item == id_item:
                self.lista_items.remove(item)
                break

    def calcular_total_general(self) ->float:
        #-Suma todos los subtotales del carrito-
        total = 0.0
        for item in self.lista_items:
            total += item.calcular_subtotal()
        return total




#--PRUEBAS--

if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL CARRITO ---")

    # 1. Creamos algunos productos de prueba
    mouse = Producto(id_producto=1, nombre="Mouse Logitech", categoria="Periféricos", precio=25000.0, stock=10)
    teclado = Producto(id_producto=2, nombre="Teclado Mecánico", categoria="Periféricos", precio=80000.0, stock=5)

    # 2. Instanciamos nuestro carrito
    mi_carrito = Carrito()

    # 3. Agregamos ítems y probamos la lógica funcional
    print(f"Stock del mouse antes de comprar: {mouse.stock}")
    mi_carrito.agregar_item(id_item=1, producto=mouse, cantidad=2)
    print(f"Stock del mouse después de agregar 2 al carrito: {mouse.stock}")

    mi_carrito.agregar_item(id_item=2, producto=teclado, cantidad=1)

    # 4. Verificamos los cálculos
    print("\n--- RESUMEN DEL CARRITO ---")
    for item in mi_carrito.lista_items:
        print(f"- {item.cantidad}x {item.nombre_producto} | Subtotal: ${item.calcular_subtotal()}")

    print(f"\nTOTAL A PAGAR: ${mi_carrito.calcular_total_general()}")

    # 5. Probamos una validación (Intentar comprar algo sin stock)
    print("\n--- PROBANDO VALIDACIONES ---")
    try:
        # Intentamos comprar 20 teclados (solo hay 5 en stock)
        mi_carrito.agregar_item(id_item=3, producto=teclado, cantidad=20)
    except ValueError as X:
        print(f"¡Validación exitosa! El sistema frenó la compra y arrojó el error: {X}")
