import subprocess

ARCHIVO_CONFIG = "servidores.txt"

def list():
    subprocess.run(["lxc", "list"])

    with open(ARCHIVO_CONFIG, "r") as file:
        cont = [line.strip() for line in file.readlines()]
        subprocess.run(["lxc", "config", "show", cont])
