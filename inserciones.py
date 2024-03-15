import requests

def cambiar_ssid_por_id(device_id, ssid, ip_servidor, puerto_servidor):
    # URL de la API de GenieACS para cambiar el SSID
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tasks?connection_request'

    # Datos a enviar en la solicitud POST
    data = {
        "name": "setParameterValues",
        "parameterValues": [
            ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID", ssid, "xsd:string"]
        ]
    }

    try:
        # Realizar la solicitud POST a la API
        requests.post(url, json=data)
        print("SSID cambiado exitosamente.")

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud para cambiar el SSID: {e}")


def cambiar_contrasena_por_id(device_id, contrasena, ip_servidor, puerto_servidor):
    # URL de la API de GenieACS para cambiar la contraseña
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tasks?connection_request'

    # Datos a enviar en la solicitud POST
    data = {
        "name": "setParameterValues",
        "parameterValues": [
            ["InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.KeyPassphrase", contrasena, "xsd:string"]
        ]
    }

    try:
        # Realizar la solicitud POST a la API
        requests.post(url, json=data)
        print("Contraseña cambiada exitosamente.")

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud para cambiar la contraseña: {e}")


def insertar_tag(device_id, ip_servidor, puerto_servidor, tag):
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tags/{tag}'
    headers = {'Content-Type': 'application/json'}
    
    try:
        requests.post(url, headers=headers)
        print(f"Tag '{tag}' insertado exitosamente para el dispositivo '{device_id}'")

    except Exception as e:
        print(f"Error de conexión: {e}")