from . import terminal
#from modules.terminal import str_deco

def get_resolution_and_size_string(index, stream):
    return f"[{index}] - {stream['format_note']} ({stream['filesize'] / 1000000:.2f}MB)"
    # stream.format_note é quase igual à: stream.resolution.split('x')[1]

def get_bitrate_and_size_string(index, stream):
    return f"[{index}] - {stream['abr']} ({stream['filesize'] / 1000000:.2f}MB)"

def get_readable_video_length(length_in_seconds):
    hours = length_in_seconds // 3600
    minutes = (length_in_seconds % 3600) // 60
    seconds = length_in_seconds % 60

    hours_str = str(hours) if hours > 9 else "0" + str(hours)
    minutes_str = str(minutes) if minutes > 9 else "0" + str(minutes)
    seconds_str = str(seconds) if seconds > 9 else "0" + str(seconds)

    return f"{hours_str}:{minutes_str}:{seconds_str}"

def get_video_data_str(video):
    return f"🎬 O vídeo {video['title']} tem {get_readable_video_length(video['duration'])} de duração e está disponível nas seguintes qualidades: "

def print_video_info(index: int, stream, col_width: int = 30, cols_amount: int = 3):
    print(get_resolution_and_size_string(index, stream).ljust(col_width), end="")
    if (index + 1) % cols_amount == 0:
        print("")

def show_video_options(info, show_all_formats=False):
    terminal.clear_terminal()
    print(get_video_data_str(info))
    terminal.print_line()
    print(" ")

    print(
        terminal.str_deco.BOLD + "🎞️  Qualidades de vídeo disponíveis para download:" + terminal.str_deco.END
    )
    print(" ")

    col_amount = 3
    col_width = 30

    if show_all_formats:
        for index, stream in enumerate(info['formats']):
            if stream['vcodec'] != 'none' and stream['acodec'] == 'none' and stream['protocol'] == 'https':
                print_video_info(index, stream, col_width, col_amount)
    else:
        qualities = {}

        for i, stream in enumerate(info['formats']):
            if stream['vcodec'] != 'none' and stream['acodec'] == 'none' and stream['protocol'] == 'https':
                # Como as qualidades são fornecidas de forma ordenada, o último vídeo da qualidade atual terá o melhor codec
                qualities[stream['format_note']] = stream
            
        for i, stream in enumerate(qualities.values()):
            print_video_info(i, stream, col_width, col_amount)

    print("\n")
    print("🔇 Para desativar o download do áudio do vídeo, digite 'm'")
    print("➡️  Para ver as opções de download 'somente áudio', digite 'a'")
    terminal.print_line()
    print(terminal.str_deco.BOLD + f"🔢 Para escolher a qualidade do vídeo, digite o número correspondente a ela." + terminal.str_deco.END)

""" 
# Verifica se a qualidade já está na lista de 
if stream['format_note'] not in qualities:
    qualities[stream['format_note']] = stream
else:
    if (stream['filesize'] > qualities[stream['format_note']]['filesize']):
        qualities[stream['format_note']] = stream
"""