# Lucía Xiaoshu García García
# Valeria Teran Cruz
# Martina Montesdeoca Luzuriaga

## OPERACIONES CREAR/EMPEZAR/LISTAR/BORRAR ##
import sys
import subprocess
import os

ARCHIVO_CONFIG = "servidores.txt"

# Verificar si se ha proporcionado un nombre de contenedor
if len(sys.argv) < 2:
    print("Uso: python3 pfinal1.py <create/start/list/delete> [num_servidores]")
    sys.exit(1)

accion = sys.argv[1]  # esto va a ser el primer argumento del comando

def crear_escenario(n):
    with open(ARCHIVO_CONFIG, "w") as file:
        for i in range(1, n + 1): # dentro del bucle for se crean n contenedores. Si no ponemos +1 carga hasta el 3 si ponemos '4'
            nombre = f"s{i}"
            print(f"Creando servidor {nombre}...")
            subprocess.run(["lxc", "init", "ubuntu:20.04", nombre])
            # Esto es para guardar si se creó con éxito...
            file.write(nombre + "\n")

        # Fuera del bucle se crean contendores como balanceador y cliente
        print("Creando balanceador lb...")
        subprocess.run(["lxc", "init", "ubuntu:20.04", "lb"])
        file.write("lb\n")

        print("Creando cliente cl...")
        subprocess.run(["lxc", "init", "ubuntu:20.04", "cl"])
        file.write("cl\n")

    print("Escenario creado correctamente.")
    subprocess.run(["lxc", "list", "--fast"])
