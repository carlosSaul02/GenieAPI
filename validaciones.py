import re

def validar_contrasena(contrasena):
    # Verificar si la contraseña tiene al menos 8 caracteres
    if len(contrasena) < 8:
        return {"False": "La contraseña debe tener al menos 8 caracteres."}
    
    # Verificar si el la contraseña tiene un maximo de 64 caracteres
    if len(contrasena) > 64:
        return {"False": "El SSID debe tener un maximo de 64 caracteres."}
    
    # Verificar si la contraseña tiene espacios en blanco
    if ' ' in contrasena:
        return {"False": "La contraseña no puede contener espacios en blanco."}
    
    # Verificar si la contraseña tiene caracteres especiales
    if not re.match("^[a-zA-Z0-9]*$", contrasena):
        return {"False": "La contraseña no puede contener caracteres especiales."}
    
    return {"True": "Contraseña válida."}


def validar_ssid(ssid):
    # Verificar si el SSID tiene al menos 8 caracteres
    if len(ssid) < 5:
        return {"False": "El SSID debe tener al menos 5 caracteres."}
    
    # Verificar si el SSID tiene un maximo de 30 caracteres
    if len(ssid) > 30:
        return {"False": "El SSID debe tener un maximo de 30 caracteres."}
    
    # Verificar si el SSID tiene espacios en blanco
    if ' ' in ssid:
        return {"False": "El SSID no puede contener espacios en blanco."}
    
    return {"True": "SSID válido."}


def validar_tag(tag):
    # Verificar si el Tag tiene al menos 8 caracteres
    if len(tag) < 4:
        return {"False": "El Tag debe tener al menos 5 caracteres."}
    
    # Verificar si el Tag tiene un maximo de 30 caracteres
    if len(tag) > 15:
        return {"False": "El Tag debe tener un maximo de 15 caracteres."}
    
    # Verificar si el Tag tiene espacios en blanco
    if ' ' in tag:
        return {"False": "El Tag no puede contener espacios en blanco."}
    
    return {"True": "Tag válido."}