import sys
import subprocess
import os
import logging
import funciones_utiles

ARCHIVO_CONFIG = "servidores.txt"

# def servidores_running():
#     print("Los contenedores estan running ¿está seguro de que quiere borrarlos? [Y/N]") 
#     ans = input() 
#     if ans == "Y":
#         return true
   
   


def delete():
    with open(ARCHIVO_CONFIG, "r") as file:
        contenedores = [line.strip() for line in file.readlines()]

    while True:
        ans = input("Si desea borrar todos los contenedores y bridges escriba TODOS.\n" 
                    "Si desea borrar un contenedor individual escriba el nombre: \n").strip()
        if ans == "TODO" or ans =="todo" or ans == "Todo":
            for c in contenedores:
                subprocess.run(["lxc", "delete", c, "--force"])
            subprocess.run(["lxc", "network", "delete", "lxdbr0"])
            subprocess.run(["lxc", "network", "delete", "lxdbr1"])
            with open(ARCHIVO_CONFIG, "w") as file:
                file.write("")

        elif ans in contenedores:
            subprocess.run(["lxc", "delete", ans, "--force"])
            # eliminarlo de la lista contenedores (esta en memoria)
            contenedores.remove(ans)
            # eliminar del archivo
            with open(ARCHIVO_CONFIG, "w") as file:
                file.write("\n".join(contenedores))

        else:
            print("Nombre no válido. Intente de nuevo")
        
    ARCHIVO_CONFIG.write(" ")   