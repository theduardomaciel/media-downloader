import os

class str_deco:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

intro_str = """       _     _                  _                     _                 _           
__   _(_) __| | ___  ___     __| | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
\ \ / / |/ _` |/ _ \/ _ \   / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 \ V /| | (_| |  __/ (_) | | (_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
  \_/ |_|\__,_|\___|\___/   \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|"""

def print_line():
    print(
        "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――"
    )

def print_intro():
    print(intro_str)
    print("")
    print("🔗 Bem-vindo ao Video Downloader!")
    print('⚙️  As configurações podem ser alteradas no arquivo: "config.ini"')
    print_line()

def print_cancel():
    print()
    print(f"{str_deco.RED}❌ Download cancelado pelo usuário.{str_deco.END}")
    exit()

def print_success(title: str, file_type: str, path: str):
    print(
        str_deco.GREEN + f"✅ O {get_file_type_str(file_type)} {title} foi baixado com sucesso e está disponível em:" + str_deco.END,
        f'"{config["download"]["default_path"]}"',
    )
    clear_terminal()
    exit()

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def progress_func(stream, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage = round(bytes_downloaded / total_size * 100, 2)

    print(
        "█" * round(bytes_downloaded / total_size * 20)
        + "░" * (20 - round(bytes_downloaded / total_size * 20)),
        f"{percentage}%",
        end="\r",
    )