# Lucía Xiaoshu García García
# Valeria Teran Cruz
# Martina Montesdeoca Luzuriaga

## OPERACIONES CREAR/EMPEZAR/LISTAR/BORRAR ##
import sys
import subprocess
import os
import logging

# archivo donde vamos a guardar y leer la información del escenario
ARCHIVO_CONFIG = "servidores.txt"

# verifica si se ha proporcionado un nombre de contenedor
if len(sys.argv) < 2:
    print("Uso: python3 pfinal1.py <create/start/list/delete> [num_servidores]")
    sys.exit(1)

accion = sys.argv[1]  # esto va a ser el primer argumento del comando --> se usa abajo en el main


# Configuración para guardar los logs en un archivo y añadirlos en cada ejecución
logging.basicConfig(
    filename='logs.log',  # Archivo donde se guardarán los logs
    level=logging.DEBUG,     # Nivel de los mensajes a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del mensaje / fecha nivel mensaje
    filemode='a'   # 'a' para añadir los nuevos logs al final del archivo (en vez de sobrescribir)
)

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
    
# configura la infraestructura de red
def configurar_redes(n):  # n --> número de servidores
    logging.info("Configurando red: creando bridges...")
    
    # creamos/comprobamos que ya existen los bridge, los configuramos
    if not existe_bridge("lxdbr1"):
        try:
            subprocess.run(["lxc", "network", "create", "lxdbr1", 
                            "ipv4.address=134.3.1.1/24", 
                            "ipv4.nat=false", 
                            "ipv6.address=none",
                            "ipv6.nat=false",
                            "dns.domain=lxd",
                            "dns.mode=none"])
            logging.info("Bridge lxdbr1 creado correctamente.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al crear el bridge lxdbr1: {e}")
            return
    else:
        logging.info("El bridge lxdbr1 ya existe.")
        subprocess.run(["lxc", "network", "set", "lxdbr1", 
                            "ipv4.address=134.3.1.1/24", 
                            "ipv4.nat=false",
                            "ipv6.address=none",
                            "ipv6.nat=false",
                            "dns.domain=lxd",
                            "dns.mode=none"])

    if not existe_bridge("lxdbr0"):
        try:
            subprocess.run(["lxc", "network", "create", "lxdbr0", 
                            "ipv4.address=134.3.0.1/24", 
                            "ipv4.nat=false", 
                            "ipv6.address=none",
                            "ipv6.nat=false",
                            "dns.domain=lxd",
                            "dns.mode=none"])
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al crear el bridge lxdbr0: {e}")
            return
    else:
        logging.info("El bridge lxdbr0 ya existe.")
        subprocess.run(["lxc", "network", "set", "lxdbr0", 
                            "ipv4.address=134.3.0.1/24", 
                            "ipv4.nat=false",
                            "ipv6.address=none",
                            "ipv6.nat=false",
                            "dns.domain=lxd",
                            "dns.mode=none"])

    # configura la red para el cliente y el balanceador
    try:
        # Cliente
        logging.info("Configurando la red para el cliente...")
        subprocess.run(["lxc", "network", "attach", "lxdbr1", "cl", "eth0"])
        subprocess.run(["lxc", "config", "device", "set", "cl", "eth0", "ipv4.address", "134.3.1.2"])

        # Balanceador: dos interfaces
        logging.info("Configurando la red para el balanceador...")
        subprocess.run(["lxc", "network", "attach", "lxdbr1", "lb", "eth0"])
        subprocess.run(["lxc", "config", "device", "set", "lb", "eth0", "ipv4.address", "134.3.1.10"])

        subprocess.run(["lxc", "network", "attach", "lxdbr0", "lb", "eth1"])
        subprocess.run(["lxc", "config", "device", "set", "lb", "eth1", "ipv4.address", "134.3.0.10"])
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al configurar las interfaces de red: {e}")
        return


    # Servidores
    try:
        for i in range(1, n + 1):
            nombre = f"s{i}"
            ip = f"134.3.0.1{i}"
            logging.info(f"Configurando la red para el servidor {nombre} con la IP {ip}...")
            subprocess.run(["lxc", "network", "attach", "lxdbr0", nombre, "eth0"])
            subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", ip])
        logging.info("Red configurada correctamente para todos los servidores.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al configurar las interfaces de los servidores: {e}")
        return
    
# MODULOS DE ACCIONES: create, start, list, delete

# modulo 1 --> crear los contenedores
def crear_escenario(n):
    with open(ARCHIVO_CONFIG, "w") as file:
        for i in range(1, n + 1): # dentro del bucle for se crean n contenedores. Si no ponemos +1 carga hasta el 3 si ponemos '4'
            nombre = f"s{i}"
            if existe_contenedor(nombre):
                logging.info(f"El contenedor {nombre} ya existe. Saltando creación.")
            else:
                subprocess.run(["lxc", "init", "ubuntu:20.04", nombre])
                # Esto es para guardar si se creó con éxito...
                file.write(nombre + "\n")

        # Fuera del bucle se crean contendores como balanceador y cliente
        if existe_contenedor("lb"):
            logging.info("El balanceador lb ya existe. Saltando creación.")
        else:
            logging.info("Creando balanceador lb...")
            subprocess.run(["lxc", "init", "ubuntu:20.04", "lb"])
            file.write("lb\n")

        if existe_contenedor("cl"):
            logging.info("El contenedor cl ya existe. Saltando creación.")
        else:
            logging.info("Creando cliente cl...")
            subprocess.run(["lxc", "init", "ubuntu:20.04", "cl"])
            file.write("cl\n")

    # llama a la configuración de red, después de crear los contenedores
    configurar_redes(n)
    logging.info("Red configurada correctamente.")


    logging.info("Escenario creado correctamente.")
    subprocess.run(["lxc", "list"])
    subprocess.run(["lxc", "list", "--fast"])

    print("Escenario creado correctamente.")
    subprocess.run(["lxc", "list", "--fast"])


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