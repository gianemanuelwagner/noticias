from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL de la API de destino
api_url = 'https://newsapi.org/v2/everything?q=tesla&from=2023-08-05&sortBy=publishedAt&apiKey=dc8b836527e24c72b09284b683d8ee6b'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construir la URL completa de la API de destino
    target_url = f'{api_url}/{path}'
    
    # Reenviar la solicitud al servidor de destino
    if request.method == 'GET':
        response = requests.get(target_url, params=request.args)
    elif request.method == 'POST':
        response = requests.post(target_url, data=request.data, headers=request.headers)
    elif request.method == 'PUT':
        response = requests.put(target_url, data=request.data, headers=request.headers)
    elif request.method == 'DELETE':
        response = requests.delete(target_url, headers=request.headers)
    else:
        return 'Método HTTP no admitido', 405
    
    # Devolver la respuesta del servidor de destino al cliente
    return (response.text, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
