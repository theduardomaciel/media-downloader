from . import terminal

def get_resolution_and_size_string(index, stream):
    return f"[{index}] - {stream.resolution} ({stream.filesize / 1000000:.2f}MB)"

def get_bitrate_and_size_string(index, stream):
    return f"[{index}] - {stream.abr} ({stream.filesize / 1000000:.2f}MB)"

def get_video_length_in_minutes(length):
    return f"{length // 60}:{length % 60:02d}"

""" 
def get_video_length_in_minutes(length_in_seconds):
    minutes = length_in_seconds // 60
    seconds = length_in_seconds % 60
    seconds_str = str(seconds) if seconds > 9 else "0" + str(seconds)

    return f"{minutes}:{seconds_str}"
"""

def get_video_data_str(video):
    return f"🎬 O vídeo {video.title} tem {get_video_length_in_minutes(video.length)} de duração e está disponível nas seguintes qualidades: "

def show_video_options(info):
    terminal.clear_terminal()
    print(get_video_data_str(info))
    terminal.print_line()
    print(" ")

    print(
        terminal.str_deco.BOLD + "🎞️  Qualidades de vídeo disponíveis para download:" + terminal.srt_deco.END
    )
    print(" ")

    col_amount = 3
    col_width = 30

    for i, stream in enumerate(info['formats']):
        if stream['vcodec'] != 'none' and stream['acodec'] == 'none':
            print(get_resolution_and_size_string(i, stream))
            if (i + 1) % col_amount == 0:
                print("")

    print("")
    print("🔇 Para desativar o download do áudio do vídeo, digite 'm'")
    print("➡️ Para ver as opções de download 'somente áudio', digite 'a'")
    terminal.print_line()
    print(terminal.str_deco.BOLD + f"🔢 Para escolher a qualidade do vídeo, digite o número correspondente a ela." + terminal.str_deco.END)