# Lucía Xiaoshu García García
# Valeria Teran Cruz
# Martina Montesdeoca Luzuriaga

## OPERACIONES CREAR/EMPEZAR/LISTAR/BORRAR ##
import sys
import subprocess
import os
import logging
from crear import crear_escenario
from list_contenedores import list
from start_escenario import start
from delete_escenario import delete

accion = sys.argv[1]  # esto va a ser el primer argumento del comando --> se usa abajo en el main

# Configuración para guardar los logs en un archivo y añadirlos en cada ejecución
logging.basicConfig(
    filename='logs.log',  # Archivo donde se guardarán los logs
    level=logging.DEBUG,     # Nivel de los mensajes a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del mensaje / fecha nivel mensaje
    filemode='a'   # 'a' para añadir los nuevos logs al final del archivo (en vez de sobrescribir)
)

# LOGICA SEGUN LA ACCION --> main

if accion == "create":
    servidores = 2  # Valor por defecto
    if len(sys.argv) == 3:
        try:
            servidores = int(sys.argv[2])
            if not (1 <= servidores <= 5):
                logging.error("El número de servidores debe estar entre 1 y 5.")
                sys.exit(1)
        except ValueError:
            logging.error("El número de servidores debe ser un entero.")
            sys.exit(1)
    crear_escenario(servidores)
    # with open("numero_contenedores", "w") as numero:
    #     numero.write(str(servidores))


if accion == "start":
    start()
    subprocess.run(["lxc", "list"])


if accion == "list":
    list()

if accion == "delete":
    delete()