class Producto:
    #-Representa un artículo tecnológico de la tienda-

    def __init__(self, id_producto: int, nombre: str, categoria: str, precio: float, stock: int) ->None:
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

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
    #-Gestiona los ítems elegisdos para la compra-

    def __init__(self) ->None:
        self.lista_items = []

    def agregar_item(self, id_item: int, producto: Producto, cantidad: int) ->None:
        #-Añade un nuevo ítem validando que haya stock y cantidad positiva-
        if cantidad <= 0:
            raise ValueError("Debe agregar al menos 1 producto.")

        if producto.hay_stock(cantidad):
            nuevo_item = ItemCarrito(id_item, producto, cantidad)
            self.lista_items.append(nuevo_item)
            producto.actualizar_stock(-cantidad) # descontamos del stock
        else:
            raise ValueError("No hay stock suficiente para este producto.")

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



