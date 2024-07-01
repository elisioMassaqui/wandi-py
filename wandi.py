import os
import subprocess
import serial.tools.list_ports
import time
import threading
from colorama import init, Fore, Back, Style

# Inicializa o colorama
init()

# Defina o diretório onde o Arduino CLI está instalado
ARDUINO_CLI_DIR = r"C:\arduino-cli"
ARDUINO_CLI_EXEC = f'"{os.path.join(ARDUINO_CLI_DIR, "arduino-cli.exe")}"'

def check_arduino_cli_exists():
    if not os.path.exists(ARDUINO_CLI_EXEC.strip('"')):
        print("Arduino CLI não encontrado. Verifique o caminho configurado.")
        input("Pressione Enter para sair...")
        exit(1)

def add_to_path():
    os.environ["PATH"] += os.pathsep + ARDUINO_CLI_DIR

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def loading_animation(duration):
    for i in range(101):
        time.sleep(duration / 100)
        blue_part = Fore.BLUE + '#' * (i // 2)
        green_part = Fore.GREEN + '-' * (50 - i // 2)
        bar = f"[{blue_part}{green_part}] {i}%"
        print(f'\r{bar}', end='', flush=True)
    print(Style.RESET_ALL)

def list_ports():
    print("Listando portas seriais disponíveis...")
    loading_animation(1)
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device} - {port.description}")
    input("Pressione Enter para voltar ao menu...")

def check_version():
    print("Verificando a versão do Arduino CLI...")
    loading_animation(1)
    run_command(f'{ARDUINO_CLI_EXEC} version')
    input("Pressione Enter para voltar ao menu...")

def upload_sketch():
    sketch_path = input("Digite o caminho completo para o sketch (.ino): ")
    if not os.path.exists(sketch_path):
        print("Caminho do sketch não encontrado. Verifique o caminho e tente novamente.")
        input("Pressione Enter para voltar ao menu...")
        return

    serial_port = input("Digite a porta serial do Arduino (ex. COM19): ")

    print("Compilando o sketch...")
    loading_animation(2)
    if run_command(f'{ARDUINO_CLI_EXEC} compile --fqbn arduino:avr:uno "{sketch_path}"') != 0:
        print("Erro ao compilar o sketch. Verifique o código.")
        input("Pressione Enter para voltar ao menu...")
        return

    print(f"Fazendo upload do sketch para o Arduino Uno na porta {serial_port}...")
    loading_animation(2)
    if run_command(f'{ARDUINO_CLI_EXEC} upload -p {serial_port} --fqbn arduino:avr:uno "{sketch_path}" -v') != 0:
        print("Erro ao fazer upload do sketch. Verifique a conexão e a porta serial.")
    else:
        print(f"Sketch compilado e carregado com sucesso para o Arduino Uno na porta {serial_port}.")
    input("Pressione Enter para voltar ao menu...")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==============================")
        print("Bem-vindo ao Script Arduino CLI")
        print("==============================")
        print("1. Listar portas seriais disponíveis")
        print("2. Verificar a versão do Arduino CLI")
        print("3. Compilar e carregar um sketch")
        print("4. Sair")
        print("==============================")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            list_ports()
        elif choice == "2":
            check_version()
        elif choice == "3":
            upload_sketch()
        elif choice == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    check_arduino_cli_exists()
    add_to_path()
    print("Atualizando índice do core...")
    loading_animation(1)
    run_command(f'{ARDUINO_CLI_EXEC} core update-index')
    print("Instalando suporte para Arduino Uno...")
    loading_animation(1)
    run_command(f'{ARDUINO_CLI_EXEC} core install arduino:avr')
    main_menu()
