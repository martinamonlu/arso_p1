import subprocess
import logging

ARCHIVO_CONFIG = "servidores.txt"

def start():
    try:
        with open(ARCHIVO_CONFIG, "r") as file:
            contenedores = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error("No se encontró el archivo de configuración. ¿Ejecutaste primero create?")
        return
    for cont in contenedores:
        logging.info(f"Iniciando contenedor {cont}...")
        subprocess.Popen(["lxc", "start", cont])
    

