import os

import configparser

config = configparser.ConfigParser(os.environ)
config.read("config.ini")

print("Bem-vindo ao YouTube Downloader!")
print("⚙️ As configurações podem ser alteradas no arquivo config.ini")

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
                ).run()
            )
        except ffmpeg.Error as e:
            # print(e.stderr)
            exit()

        os.remove("audio.mp4")
        os.remove(stream.default_filename)

        try:
            os.rename(stream.default_filename[:-4] + "_final.mp4", output_path)
        except FileExistsError:
            os.remove(output_path)
            os.rename(stream.default_filename[:-4] + "_final.mp4", output_path)

        print(
            f"✅ O vídeo {stream.title} foi baixado com sucesso e está disponível em:",
            f'"{config["download"]["default_path"]}"',
        )
        exit()
    else:
        if stream.includes_video_track and stream.is_progressive == False:
            # print("Baixando áudio do vídeo separadamente...")
            audio_stream = (
                yt.streams.filter(only_audio=True, mime_type="audio/mp4")
                .order_by("abr")
                .desc()[0]
            )
            audio_stream.download(filename="audio.mp4")
        else:
            if stream.includes_video_track:
                print(
                    f"✅ O vídeo {stream.title} foi baixado com sucesso e está disponível em:",
                    f'"{config["download"]["default_path"]}"',
                )
            else:
                print(
                    f"✅ O áudio do vídeo {stream.title} foi baixado com sucesso e está disponível em:",
                    f'"{config["download"]["default_path"]}"',
                )

            exit()


try:
    yt = YouTube(
        input("🔗 Insira o link do vídeo que você deseja baixar: "),
        on_progress_callback=progress_func,
        on_complete_callback=complete_func,
    )
except KeyboardInterrupt:
    print("")
    print("❌ Download cancelado pelo usuário.")
    exit()
except VideoUnavailable:
    print("☹️ O vídeo que você digitou não está disponível :(")
    exit()

print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")
print("🔄 Obtendo dados do vídeo...")

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


print(
    f"🎬 O vídeo {yt.title} tem {get_video_length_in_minutes(yt.length)} de duração e está disponível nas seguintes qualidades: "
)

print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")

print("🎞️ Qualidades de vídeo disponíveis: ")
for i in range(len(mp4_streams)):
    print(
        f"[{i}] - {mp4_streams[i].resolution} ({mp4_streams[i].filesize / 1000000:.2f}MB)"
    )
    # print(mp4_streams[i])

print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")

print("🔈Qualidades de áudio disponíveis: ")
for i in range(len(mp4_streams), len(mp4_streams) + len(mp3_streams)):
    print(
        f"[{i}] - {mp3_streams[i - len(mp4_streams)].abr} ({mp3_streams[i - len(mp4_streams)].filesize / 1000000:.2f}MB)"
    )
    # print(mp3_streams[i - len(mp4_streams)])

print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")

quality_input = int(input("❓Qual qualidade você deseja baixar? "))

while quality_input < 0 or quality_input >= len(streams):
    try:
        quality_input = int(input("❓Qual qualidade você deseja baixar? "))
    except KeyboardInterrupt:
        print("")
        print("❌ Download cancelado pelo usuário.")
        exit()

stream = streams[int(quality_input)]

print(
    f"➡️ Você escolheu baixar o vídeo na qualidade {stream.resolution} ({stream.filesize / 1000000:.2f}MB)."
)

if stream.includes_video_track and stream.is_progressive == False:
    # print("O vídeo não é progressivo, então o áudio será baixado separadamente e juntado ao vídeo.")
    stream.download()
else:
    stream.download(config["download"]["default_path"])
