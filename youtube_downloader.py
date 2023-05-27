import os

import configparser

config = configparser.ConfigParser(os.environ)
config.read("config.ini")

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

def print_line():
    print(
        "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――"
    )


def print_cancel():
    print("")
    print(str_deco.RED + "❌ Download cancelado pelo usuário." + str_deco.END)
    exit()


def print_success(title):
    print(
        str_deco.GREEN + f"✅ O {get_file_type_str(file_type)} {title} foi baixado com sucesso e está disponível em:" + str_deco.END,
        f'"{config["download"]["default_path"]}"',
    )
    clear_terminal()
    exit()

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

intro_str = """ __   __  _______  __   __  _______  __   __  _______  _______    ______   _______  _     _  __    _  ___      _______  _______  ______   _______  ______   
|  | |  ||       ||  | |  ||       ||  | |  ||  _    ||       |  |      | |       || | _ | ||  |  | ||   |    |       ||   _   ||      | |       ||    _ |  
|  |_|  ||   _   ||  | |  ||_     _||  | |  || |_|   ||    ___|  |  _    ||   _   || || || ||   |_| ||   |    |   _   ||  |_|  ||  _    ||    ___||   | ||  
|       ||  | |  ||  |_|  |  |   |  |  |_|  ||       ||   |___   | | |   ||  | |  ||       ||       ||   |    |  | |  ||       || | |   ||   |___ |   |_||_ 
|_     _||  |_|  ||       |  |   |  |       ||  _   | |    ___|  | |_|   ||  |_|  ||       ||  _    ||   |___ |  |_|  ||       || |_|   ||    ___||    __  |
  |   |  |       ||       |  |   |  |       || |_|   ||   |___   |       ||       ||   _   || | |   ||       ||       ||   _   ||       ||   |___ |   |  | |
  |___|  |_______||_______|  |___|  |_______||_______||_______|  |______| |_______||__| |__||_|  |__||_______||_______||__| |__||______| |_______||___|  |_|"""

print(intro_str)
print("")
print('⚙️  As configurações podem ser alteradas no arquivo: "config.ini"')
print_line()

from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pytube.helpers import safe_filename

file_type = config["download"]["default_filetype"]

def progress_func(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage = round(bytes_downloaded / total_size * 100, 2)

    print(
        "█" * round(bytes_downloaded / total_size * 20)
        + "░" * (20 - round(bytes_downloaded / total_size * 20)),
        f"{percentage}%",
        end="\r",
    )

    # print("{:00.0f}% downloaded".format(bytes_downloaded / total_size * 100))


import ffmpeg

is_video_audio_download_enabled = True

def get_file_type_str(file_type):
    return file_type == "video" and "vídeo" or "áudio"

def complete_func(stream, file_path):
    output_path = config["download"]["default_path"] + "/" + stream.default_filename

    if (
        "audio.mp4" in file_path
        and stream.includes_audio_track
        and not stream.includes_video_track
    ):
        # print("Juntando áudio e vídeo...")
        try:
            (
                ffmpeg.output(
                    ffmpeg.input("audio.mp4"),
                    ffmpeg.input(stream.default_filename),
                    stream.default_filename[:-4] + "_final.mp4",
                    vcodec="copy",
                    acodec="copy",
                    strict="experimental",
                    loglevel="quiet",
                ).run()
            )
        except ffmpeg.Error as e:
            print(e.stderr)
            print(
                "❌ Ocorreu um erro ao juntar o áudio e o vídeo. Envie o log do erro acima para o desenvolvedor."
            )
            exit()

        os.remove("audio.mp4")
        os.remove(stream.default_filename)

        try:
            os.rename(stream.default_filename[:-4] + "_final.mp4", output_path)
        except FileExistsError:
            os.remove(output_path)
            os.rename(stream.default_filename[:-4] + "_final.mp4", output_path)

        print_success(stream.title)
        exit()
    else:
        if (
            stream.includes_video_track
            and stream.is_progressive == False
            and is_video_audio_download_enabled
        ):
            # print("Baixando áudio do vídeo separadamente...")
            audio_stream = (
                yt.streams.filter(only_audio=True, mime_type="audio/mp4")
                .order_by("abr")
                .desc()[0]
            )
            audio_stream.download(filename="audio.mp4")
        else:
            print_success(stream.title)


def get_youtube():
    try:
        return YouTube(
            input(str_deco.BOLD + "🔗 Insira o link do vídeo que você deseja baixar: " + str_deco.END),
            on_progress_callback=progress_func,
            on_complete_callback=complete_func,
        )
    except KeyboardInterrupt:
        print_cancel()
    except VideoUnavailable:
        print(
            str_deco.YELLOW + "☹️ O vídeo que você digitou não está disponível. Por favor, tente outro." + str_deco.END
        )
        return get_youtube()
    except Exception as e:
        # print(e)
        print(
            "☹️  Ocorreu um erro ao tentar baixar o vídeo. Verifique se o link está correto e tente novamente."
        )
        return get_youtube()


yt = get_youtube()

clear_terminal()
print(str_deco.DARK_CYAN + str_deco.BOLD + "🔄 Obtendo dados do vídeo..." + str_deco.END)

mp4_streams = (
    yt.streams.filter(file_extension="mp4", only_video=True)
    .order_by("resolution")
    .desc()
)
mp3_streams = (
    yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").desc()
)
streams = list(mp4_streams) + list(mp3_streams)


def get_video_length_in_minutes(length_in_seconds):
    minutes = length_in_seconds // 60
    seconds = length_in_seconds % 60
    seconds_str = str(seconds) if seconds > 9 else "0" + str(seconds)

    return f"{minutes}:{seconds_str}"


def get_video_data_str():
    return f"🎬 O vídeo {yt.title} tem {get_video_length_in_minutes(yt.length)} de duração e está disponível nas seguintes qualidades: "

print_line()

import msvcrt

def request_input():
    try:
        global input
        # input = msvcrt.getche().decode('ASCII')
        input = msvcrt.getwch()
    except KeyboardInterrupt:
        print_cancel()

def get_resolution_and_size_string(index, stream):
    return f"[{index}] - {stream.resolution} ({stream.filesize / 1000000:.2f}MB)"

def get_bitrate_and_size_string(index, stream):
    return f"[{index}] - {stream.abr} ({stream.filesize / 1000000:.2f}MB)"

def show_video_options():
    clear_terminal()
    print(get_video_data_str())
    print_line()
    print(" ")

    print(
       str_deco.BOLD + "🎞️  Qualidades de vídeo disponíveis para download:" + str_deco.END
    )
    print(" ")

    col_amount = 3
    col_width = 30

    for i in range(len(mp4_streams)):
        print(get_resolution_and_size_string(i, mp4_streams[i]).ljust(col_width), end="")

        if (i + 1) % col_amount == 0:
            print("")

    print("")
    print("🔇 Para desativar o download do áudio do vídeo, digite 'm'")
    print("➡️ Para ver as opções de download 'somente áudio', digite 'a'")
    print_line()
    print(str_deco.BOLD + f"🔢 Para escolher a qualidade do {get_file_type_str(file_type)}, digite o número correspondente a ela." + str_deco.END)

def show_audio_options():
    clear_terminal()
    print(get_video_data_str())
    print_line()
    print(" ")

    print(
       str_deco.BOLD + "🔈 Qualidades de áudio disponíveis para download:." + str_deco.END
    )
    print(" ")

    col_amount = 3
    col_width = 30

    for i in range(len(mp3_streams)):
        print(get_bitrate_and_size_string(i, mp3_streams[i]).ljust(col_width), end="")

        if (i + 1) % col_amount == 0:
            print("")

    print("")
    print("➡️ Para ver as opções de download de vídeo, digite 'v'")
    print_line()
    print(str_deco.BOLD + f"🔢 Para escolher a qualidade do {get_file_type_str(file_type)}, digite o número correspondente a ela." + str_deco.END)

if file_type == "video":
    show_video_options()
elif file_type == "audio":
    show_audio_options()
else:
    print(
        "❌ Erro: Tipo de arquivo especificado nas configurações (config.ini) inválido."
    )

request_input()

while ((not input.isdigit()) or (int(input) < 0 or int(input) >= len(streams))):
    if not input.isdigit():
        match input:
            case "m":
                if is_video_audio_download_enabled:
                    is_video_audio_download_enabled = False
                    print("🔇 O download do áudio do vídeo foi desativado.")
                else:
                    is_video_audio_download_enabled = True
                    print("🔊 O download do áudio do vídeo foi ativado.")

                request_input()
                
            case "a":
                file_type = "audio"
                show_audio_options()
                request_input()
                
            case "v":
                file_type = "video"
                show_video_options()
                request_input()
            case "q":
                print_cancel()
                
            case _:
                print("❌ A opção selecionada é inválida. Tente novamente.")
                request_input()
                
    else:
       request_input()

stream = streams[file_type == "video" and int(input) or int(input) - len(mp4_streams)]

print(
    f"➡️ Você escolheu baixar o {get_file_type_str(file_type)} na qualidade {stream.resolution} ({stream.filesize / 1000000:.2f}MB)."
)

if (
    stream.includes_video_track
    and stream.is_progressive == False
    and is_video_audio_download_enabled
):
    # print("O vídeo não é progressivo, então o áudio será baixado separadamente e juntado ao vídeo.")
    stream.download()
else:
    stream.download(config["download"]["default_path"])
