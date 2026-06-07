from flask import Flask
import base_de_datos
import modelos

# Inicializamos la aplicación Flask
app = Flask(__name__)

#TEMPORAL...
# Definimos nuestra primera "Ruta" (Endpoint)
@app.route('/')
def inicio():
    """Esta función se ejecuta cuando entramos a la página principal."""
    # Por ahora, solo devolveremos un texto simple para comprobar la conexión
    return "<h1>El servidor conecto. xD</h1>"

x = """
posible reemplazo de @app.route('/')
from flask import render_template

@app.route('/')
def inicio():
    #Esta función se ejecuta cuando entramos a la página principal
    # 1. Le pedimos a la base de datos la lista de productos
    conexion = base_datos.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    catalogo = cursor.fetchall()
    conexion.close()

    # 2. En lugar de un texto, devolvemos un archivo HTML completo
    # y le pasamos el catálogo para que dibuje la tabla.
    return render_template('index.html', productos=catalogo)
"""

# --- EJECUCIÓN DEL SERVIDOR ---
if __name__ == '__main__':
    # debug=True hace que el servidor se reinicie solo si detecta cambios en el código
    app.run(debug=True)
