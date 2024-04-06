import msvcrt
from . import terminal
#from modules.terminal import str_deco

def get_resolution_and_size_string(index, stream):
    return f"[{index}] - {stream['format_note']} ({stream['filesize'] / 1000000:.2f}MB)"

def get_bitrate_and_size_string(index, stream):
    return f"[{index}] - {stream['abr']} ({stream['filesize'] / 1000000:.2f}MB)"

def get_readable_media_length(length_in_seconds):
    hours = length_in_seconds // 3600
    minutes = (length_in_seconds % 3600) // 60
    seconds = length_in_seconds % 60

    hours_str = str(hours) if hours > 9 else "0" + str(hours)
    minutes_str = str(minutes) if minutes > 9 else "0" + str(minutes)
    seconds_str = str(seconds) if seconds > 9 else "0" + str(seconds)

    return f"{hours_str}:{minutes_str}:{seconds_str}"

def get_media_data_str(media):
    return f"🎬 O vídeo {media['title']} tem {get_readable_media_length(media['duration'])} de duração e está disponível nas seguintes qualidades: "

def print_vertically(streams: list, cols_amount: int = 3, col_width: int = 30):
    # Imprimimos as qualidades de vídeo disponíveis verticalmente, de forma que o usuário possa ler de cima para baixo de coluna em coluna
    for i in range(len(streams) // cols_amount + 1):
        for j in range(cols_amount):
            index = i + j * (len(streams) // cols_amount)
            if index < len(streams):
                print(get_resolution_and_size_string(index, streams[index]).ljust(col_width), end="")
        print()

def is_valid_media(stream, file_type: str):
    return stream['protocol'] == 'https' and file_type == 'video' and stream['vcodec'] != 'none' or stream['protocol'] == 'https' and file_type == 'audio' and stream['audio_ext'] != 'none' and stream['resolution'] == 'audio only' and stream['acodec'] != 'none'
    # stream['vcodec'] != 'none' and stream['acodec'] == 'none' and stream['protocol'] == 'https' and (file_type == 'audio' and stream['resolution'] == 'audio only')

def show_media_options(info, file_type: str, show_all_codecs=False, is_media_audio_enabled=True):
    terminal.clear_terminal()
    print(get_media_data_str(info))
    terminal.print_line()
    print(" ")

    if file_type == 'video':
        print(
            terminal.str_deco.BOLD + "🎞️  Qualidades de vídeo disponíveis para download:" + terminal.str_deco.END
        )
    elif file_type == 'audio':
        print(
            terminal.str_deco.BOLD + "🔊 Qualidades de áudio disponíveis para download:" + terminal.str_deco.END
        )

    if show_all_codecs:
        print(f"{terminal.str_deco.RED}🔴 Atenção: Todos os codecs estão sendo exibidos. Para alterar esse comportamento, altere as configurações.{terminal.str_deco.END}")
    print(" ")

    col_amount = 3
    col_width = 30

    streams = []

    if show_all_codecs:
        for index, stream in enumerate(info['formats']):
            if is_valid_media(stream, file_type):
                streams.append(stream)
    else:
        qualities = {}

        for i, stream in enumerate(info['formats']):
            if is_valid_media(stream, file_type):
                # Como as qualidades são fornecidas de forma ordenada, o último vídeo da qualidade atual terá o melhor codec
                qualities[stream['format_note']] = stream
            
        for index, quality in enumerate(qualities):
            streams.append(qualities[quality])

    print_vertically(streams, col_amount, col_width)

    print("")
    
    if file_type == 'video':
        if is_media_audio_enabled:
                print(f"🔈 O download do áudio está {terminal.str_deco.BOLD}{terminal.str_deco.GREEN}ATIVADO{terminal.str_deco.END}. Para desativar, aperte 'm'") 
        else:
            print(f"🔇 O download do áudio está {terminal.str_deco.BOLD}{terminal.str_deco.RED}DESATIVADO{terminal.str_deco.END}. Para ativar, aperte 'm'")

    
    if file_type == 'audio':
        print("🎞️  Para ver as opções de download de vídeo, digite 'a'")
    else:
        print("➡️  Para ver as opções de download 'somente áudio', digite 'a'")

    terminal.print_line()

    print(f"{terminal.str_deco.BOLD}🔢 Para escolher a qualidade do {file_type == 'video' and "vídeo" or "áudio"}, digite o número correspondente a ela.{terminal.str_deco.END}")

    return streams

def request_media_quality(info, file_type: str, show_all_codecs=False, is_media_audio_enabled=True):
    streams = show_media_options(info, file_type, show_all_codecs, is_media_audio_enabled)

    option = None

    while True:
        try:
            option = msvcrt.getwch()

            if option == 'q':
                terminal.print_cancel()
                break

            if option == 'm' and file_type == 'video':
                is_media_audio_enabled = not is_media_audio_enabled
                streams = show_media_options(info, file_type, show_all_codecs, is_media_audio_enabled)
                continue
            elif option == 'a':
                new_file_type = file_type == 'video' and 'audio' or 'video'
                show_media_options(info, new_file_type, show_all_codecs, is_media_audio_enabled)
                continue
            
            media_quality = int(option)

            if media_quality < 0 or media_quality >= len(streams):
                print(f"{terminal.str_deco.RED}🔴 Por favor, insira um número válido.{terminal.str_deco.END}")
                continue
            else:
                option = media_quality
                break
        except UnicodeDecodeError:
                continue
        except ValueError:
            print(f"{terminal.str_deco.RED}🔴 Por favor, insira um número válido.{terminal.str_deco.END}")
            continue
        except KeyboardInterrupt:
            terminal.print_cancel()
            break
    
    return streams[media_quality]