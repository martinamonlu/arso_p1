import sys
import subprocess
import os
import logging

# verifica si un contenedor existe
def existe_contenedor(nombre):
    logging.info(f"Verificando si el contenedor {nombre} existe...")
    result = subprocess.run(["lxc", "list", nombre], capture_output=True, text=True)
    return nombre in result.stdout

# verificarç si un bridge existe
def existe_bridge(nombre):
    logging.info(f"Verificando si el bridge {nombre} existe...")
    try:
        # Ejecutar el comando `lxc network list` para verificar si el bridge existe
        result = subprocess.run(["lxc", "network", "list"], capture_output=True, text=True)
        if nombre in result.stdout:
            return True
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al verificar el bridge {nombre}: {e}")
        return False