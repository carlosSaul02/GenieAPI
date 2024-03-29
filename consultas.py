import requests
import datetime

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
    




def refrescar_dispositivo(device_id, ip_servidor, puerto_servidor):
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tasks?connection_request'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'name': 'refreshObject',
        'objectName': ''
    }
    print("Refrescando Dispositivo...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Verificar si hay errores en la respuesta

        # Imprimir la respuesta
        print("Parametros actualizados!!")
        #print(response.text)
               

    except requests.exceptions.RequestException as e:
        print("Error al hacer la consulta:", e)
        return None
    

def reiniciar_dispositivo(device_id, ip_servidor, puerto_servidor):
    url = f'http://{ip_servidor}:{puerto_servidor}/devices/{device_id}/tasks?timeout=3000&connection_request'
    payload = {"name": "reboot"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Exito! Dispositivo reiniciado.")
        else:
            print(f"Error al reiniciar dispositivo. Código de estado: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None