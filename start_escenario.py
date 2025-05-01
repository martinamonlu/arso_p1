import subprocess
import logging

ARCHIVO_CONFIG = "servidores.txt"
ARCHIVO_RUN = "contenedores_running.txt"

def start():

    with open(ARCHIVO_CONFIG, "r") as file:
        contenedores = [line.strip() for line in file.readlines()]
    # with open(ARCHIVO_RUN, "a"):
    #     pass
    

    # try:
    #     with open(ARCHIVO_CONFIG, "r") as file:
    #         contenedores = [line.strip() for line in file.readlines()]
    # except FileNotFoundError:
    #     logging.error("No se encontró el archivo de configuración. ¿Ejecutaste primero create?")
    #     return
     

    while True:
        ans = input("Si desea arrancar todos los contenedores escriba TODOS.\n" 
                    "Si desea arancar un contenedor individual escriba el nombre: \n"
                    "Si desea salir escriba S \n").strip()
        if ans == "TODOS" or ans =="todos" or ans == "Todos":
            for c in contenedores: # recorremos los contenedores
                with open(ARCHIVO_RUN, "r") as file: # leemos el archivo contenedores_running.txt
                    c_run = [line.strip() for line in file.readlines()]
                if c in c_run: # si el contenedor esta en el archivo contenedores_running.txt
                    print(f"El contenedor {c} ya esta arrancado")
                else:
                    logging.info(f"Iniciando contenedor {c}...")
                    subprocess.Popen(["lxc", "start", c])
                    with open(ARCHIVO_RUN, "a") as file:
                        file.write(f"{c}\n")

        elif ans in contenedores:
            with open(ARCHIVO_RUN, "r") as file:
                c_run = [line.strip() for line in file.readlines()]
            
            if ans in c_run:
                print(f"el contenedor {ans} ya esta arrancado")
            else:    
                logging.info(f"Iniciando contenedor {ans}...")
                subprocess.run(["lxc", "start", ans])
                with open(ARCHIVO_RUN, "w") as file:
                    file.write(f"{ans}\n")

        elif ans == "s" or ans == "S":
            return

        else:
            print("Nombre no válido. Intente de nuevo")
        

