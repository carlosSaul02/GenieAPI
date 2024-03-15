import requests
import datetime
from validaciones import validar_tag, validar_ssid, validar_contrasena 

def obtener_id_por_serial_number(serial_number,ip_servidor,puerto_servidor):
    # URL de la API de GenieACS para buscar por SerialNumber
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/?query=%7B%22_deviceId._SerialNumber%22%3A%22{serial_number}%22%7D'

    try:
        # Realizar la consulta GET a la API
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hay errores en la respuesta

        # Convertir la respuesta JSON en un diccionario Python
        data = response.json()

        # Verificar si se encontró algún dispositivo
        if data and isinstance(data, list):
            # Tomar el primer dispositivo de la lista
            dispositivo = data[0]
            return dispositivo['_id']  # Retornar el ID del dispositivo

        else:
            print("No se encontró ningún dispositivo con ese SerialNumber.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a la API: {e}")
        return None
    


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


def obtener_informacion_dispositivo(device_id, ip_servidor, puerto_servidor):
    # URL de la API de GenieACS para obtener información del dispositivo
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/?query=%7B%22_id%22%3A%22{device_id}%22%7D'
    try:
        # Realizar la consulta GET a la API
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hay errores en la respuesta

        # Convertir la respuesta JSON en un diccionario Python
        data = response.json()

        # Verificar si se encontró algún dispositivo
        if data and isinstance(data, list):

            # Tomar el primer dispositivo de la lista
            dispositivo = data[0]
            print("****************INFORMACION DEL DISPOSITIVO***************")

            #id del dispositivo
            id_dispositivo = dispositivo['_id']
            print(f"ID: {id_dispositivo}") 

            #Serial number
            serial_dispositivo = dispositivo['_deviceId']['_SerialNumber']
            print(f"Serial Number: {serial_dispositivo}")

            # Retornar el SSID del dispositivo
            ssid_dispositivo = dispositivo['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['SSID']['_value'] 
            print(f"SSID: {ssid_dispositivo}")  

            # Retornar la contrasena del dispositivo
            contrasena_dispositivo = dispositivo['InternetGatewayDevice']['LANDevice']['1']['WLANConfiguration']['1']['KeyPassphrase']['_value'] 
            print(f"Contrasena: {contrasena_dispositivo}")  
            
            # Retornar la IP del dispositivo
            ip_dispositivo = dispositivo['InternetGatewayDevice']['WANDevice']['1']['WANConnectionDevice']['1']['WANIPConnection']['1']['ExternalIPAddress']['_value']
            print(f"IP: {ip_dispositivo}") 

            # Retornar la MAC del dispositivo
            mac_dispositivo = dispositivo['InternetGatewayDevice']['WANDevice']['1']['WANConnectionDevice']['1']['WANIPConnection']['1']['MACAddress']['_value'] 
            print(f"MAC: {mac_dispositivo}") 

            # La version de firmware
            firmware_dispositivo = dispositivo['InternetGatewayDevice']['DeviceInfo']['SoftwareVersion']['_value']
            print(f"Firmware: {firmware_dispositivo}") 
            print('\n')

            print("*********************HOSTS********************************")
            for host_key, host_info in dispositivo['InternetGatewayDevice']['LANDevice']['1']['Hosts']['Host'].items():
                if isinstance(host_info, dict):  # Verificar si es un diccionario válido
                    host_ip = host_info['IPAddress']['_value']
                    host_mac = host_info['MACAddress']['_value']
                    host_name = host_info['HostName']['_value'] if host_info['HostName']['_value'] else "Desconocido"
                    print(f"Host {host_key}:")
                    print(f"   - Nombre: {host_name}")
                    print(f"   - IP: {host_ip}")
                    print(f"   - MAC: {host_mac}")
                    print('\n')
                else:
                    print("No hay más hosts.")
                    print('\n')
                    break


            #INFORMACION DE REPORTE
            print("*****************REPORTE CON GENIE************************")
            print(f"Intervalo de reporte con el servidor: {dispositivo['InternetGatewayDevice']['ManagementServer']['PeriodicInformInterval']['_value']}s") # Retornar el PeriodicInformInterval del dispositivo
            
            #Agregar formato a _lastBoot
            last_boot_string = dispositivo['_lastBoot']
            last_boot_datetime = datetime.datetime.strptime(last_boot_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_boot = last_boot_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Ultimo Inicio: {last_boot}") #ultimo inicio
            
            #Agregar formato a _lastBootstrap
            last_bootstrap_string = dispositivo['_lastBootstrap']
            last_bootstrap_datetime = datetime.datetime.strptime(last_bootstrap_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_bootstrap = last_bootstrap_datetime.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Primer Inicio: {last_bootstrap}") #Primer inicio
            print('\n')      
        else:
            print("No se encontró ningún dispositivo con ese SerialNumber.")
            return None

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Error al hacer la solicitud a la API: {e}")
        return None


def insertar_tag(device_id, ip_servidor, puerto_servidor, tag):
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tags/{tag}'
    headers = {'Content-Type': 'application/json'}
    
    try:
        requests.post(url, headers=headers)
        print(f"Tag '{tag}' insertado exitosamente para el dispositivo '{device_id}'")

    except Exception as e:
        print(f"Error de conexión: {e}")




def main():
    serial_number = "CDKT2AC04F27"
    ip_servidor = "192.168.77.203"
    puerto_servidor = "7557"
    #device_id = "E89FEC-FTTH-CDKT2AD24296"


    #************************** Obtener el ID del dispositivo usando el SerialNumber
    device_id = obtener_id_por_serial_number(serial_number, ip_servidor, puerto_servidor)


    #************************** Obtener informacion general del dispositivo
    #obtener_informacion_dispositivo(device_id, ip_servidor, puerto_servidor)


    #************************** Cambiar el SSID del dispositivo usando su ID
    ssid = "PRUEBA"
    es_valida1 = validar_ssid(ssid)
    if "True" in es_valida1:
        print("El SSID es válido.")
        cambiar_ssid_por_id(device_id, ssid, ip_servidor, puerto_servidor)
    else:
        print("El SSID no es válido:", es_valida1["False"])


    #************************** Cambiar el CONTRASENA del dispositivo usando su ID
    contrasena = "FARAJUEGAROBLOX12"
    es_valida = validar_contrasena(contrasena)
    if "True" in es_valida:
        print("La contraseña es válida.")
        cambiar_contrasena_por_id(device_id, contrasena, ip_servidor, puerto_servidor)
    else:
        print("La contraseña no es válida:", es_valida["False"])


    #************************** Cambiar el CONTRASENA del dispositivo usando su ID



    #************************** Insertar Tag
    #tag = "prueba"
    #es_valida2 = validar_tag(tag)
    #if "True" in es_valida2:
    #    print("El Tag es válido.")
    #    insertar_tag(device_id, ip_servidor, puerto_servidor, tag)
    #else:
    #    print("El Tag no es válido:", es_valida2["False"])
    
    
    


if __name__ == "__main__":
    main()




