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
        cont = [line.strip() for line in file.readlines()]
        subprocess.run(["lxc", "delete", "--force"])
        # subprocess.run(["lxc", "network", "delete", "lxdbr0"])
        subprocess.run(["lxc", "network", "delete", "lxdbr1"])

        ARCHIVO_CONFIG.write(" ")