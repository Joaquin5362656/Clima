from flask import Flask, render_template, request
import requests


# Creamos una instancia de la aplicacion
app = Flask(__name__)

#definimos la ruta
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Función que maneja las solicitudes GET y POST a la ruta raiz ('/') de la aplicacion.
    Si la solicitud es POST, obtiene los datos del formulario, realiza una solicitud a la API
    del clima para obtener el clima actual de la ciudad y pais especificados, y luego
    renderiza index.html con los datos del clima obtenidos.
    Si la solicitud es GET, simplemente renderiza el 'index.html'.
    """
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        api_key = '4938942768ad50b61c04b7d258a168fa'  
        # Construimos la URL para la solicitud a la API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&appid={api_key}&units=metric'
        
        try:
            """
            Intentamos realizar la solicitud a la API, lanzamos una excepcion si la solicitud no fue exitosa.
            Convertimos la respuesta en formato json y extraemos los datos relevantes y alamacenamos en un diccionario 'clima'.
            """
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            print("Respuesta de la API:", data)
            clima = {
                'ciudad': ciudad,
                'temperatura': data['main']['temp'],
                'descripcion': data['weather'][0]['description']
            }
            return render_template('index.html', clima=clima)
        except requests.exceptions.RequestException as e:
            """
            Si hubo algun error durante la solicitud a la API, mostramos un msj de error
            """
            error_message = f"Error al obtener datos del clima: {e}"
            return render_template('index.html', error_message=error_message)
    

    #renderizamos el 'index.html' en el caso de solicitud Get
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
