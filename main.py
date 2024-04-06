import os
import configparser
from ffmpeg import FFmpeg
from yt_dlp import YoutubeDL

import modules.terminal as terminal
import modules.media as media

#
terminal.print_intro()

# Configurações
config = configparser.ConfigParser(os.environ)
config.read("config.ini")

file_type = config["DOWNLOAD"]["default_filetype"]
is_video_audio_enabled = config["DOWNLOAD"]["disable_video_audio"] != "True"
show_logs = config["DOWNLOAD"]["show_logs"] == "True"

URLS = config['DOWNLOAD']['urls'].split('\n')
if len(URLS) == 1 and URLS[0] == '':
    URLS = []
    try:
        while True:
            if len(URLS) > 1:
                if URLS[len(URLS) - 1] == URLS[len(URLS) - 2]:
                    URLS.pop()
                    print("URL já adicionada.")
                else:
                    print("URLs adicionadas:")
                    for URL in URLS:
                        print(URL)
                    print("")

            URL = input(f"{terminal.srt_deco.BOLD}Digite a URL do vídeo que deseja baixar{terminal.srt_deco.END} (ou 'r' para remover a anterior, 'q' para terminar): ")

            if URL == 'q':
                break

            if URL == 'r':
                if len(URLS) > 0:
                    URLS.pop()
                    print(f"{terminal.srt_deco.RED}Última URL removida.{terminal.srt_deco.END}")
                else:
                    print("Nenhuma URL adicionada.")

            URLS.append(URL)
    except KeyboardInterrupt:
        terminal.print_cancel()
        exit()

""" 
ffmpeg = (
        FFmpeg()
        .option("y")
        .input("input.mp4")
        .output(
            "output.mp4",
            {"codec:v": "libx264"},
            vf="scale=1280:-1",
            preset="veryslow",
            crf=24,
        )
    )

    ffmpeg.execute()
"""

class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def progress_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')

def format_refiner(ctx):
    # formatos são ordenados dos piores para os melhores
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    # These are the minimum required fields for a merged format
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

ydl_opts = {
    'format': format_refiner,
    'outtmpl': '%(title)s.%(ext)s',
    #'quiet': not show_logs,
    'noplaylist': True,
    'logger': Logger(),
    'progress_hooks': [progress_hook],
}


# Funções
def main():
    with YoutubeDL(ydl_opts) as ytdl:
        for URL in URLS:
            info = ytdl.extract_info(URL, download=False)
            
            # Exibimos as qualidades de vídeo disponíveis para o usuário escolher
            media.show_video_options(info)

    # show_video_options()


if __name__ == "__main__":
    main()