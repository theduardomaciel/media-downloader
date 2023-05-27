# YouTube Video Downloader

Este é um programa em Python que permite baixar vídeos do YouTube. Ele oferece a opção de escolher entre diferentes qualidades de vídeo e também permite baixar apenas o áudio.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados em seu sistema:

-   Python 3.x
-   Biblioteca `pytube` (instalável via `pip install pytube`)
-   ffmpeg.exe (disponível em https://github.com/BtbN/FFmpeg-Builds/releases)

## Instalação

1. Clone este repositório ou faça o download dos arquivos em formato ZIP.

2. Navegue até o diretório do projeto.

3. Instale as dependências necessárias executando o seguinte comando:

    ```shell
    pip install pytube
    ```

4. Insira o executável do ffmpeg `(ffmpeg.exe)` na raiz do projeto.

## Uso

1. Execute o script `youtube_downloader.py`.

2. Você será solicitado a fornecer o URL do vídeo do YouTube que deseja baixar.

3. Escolha a opção de qualidade desejada para o vídeo. Se quiser baixar apenas o áudio, selecione a opção correspondente.

4. Aguarde enquanto o programa faz o download do vídeo ou áudio selecionado.

5. O arquivo baixado será salvo no diretório do projeto.

## Exemplo

Aqui está um exemplo de uso do programa:

```shell
$ python youtube_downloader.py

Bem-vindo ao YouTube Downloader!
⚙️ As configurações podem ser alteradas no arquivo config.ini
🔗 Insira o link do vídeo que você deseja baixar: https://www.youtube.com/watch?v=dQw4w9WgXcQ
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
🔄 Obtendo dados do vídeo...
🎬 O vídeo tem 3:32 de duração e está disponível nas seguintes qualidades:
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
🎞️ Qualidades de vídeo disponíveis:
[0] - 1080p (78.66MB)
[1] - 720p (16.60MB)
[2] - 480p (8.65MB)
[3] - 360p (5.66MB)
[4] - 240p (3.01MB)
[5] - 144p (1.86MB)
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
🔈Qualidades de áudio disponíveis:
[6] - 160kbps (3.44MB)
[7] - 70kbps (1.63MB)
[8] - 50kbps (1.23MB)
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
❓Qual qualidade você deseja baixar? 0
➡️ Você escolheu baixar o vídeo na qualidade 1080p (78.66MB).

✅ O vídeo foi baixado com sucesso.
```

## Contribuição

Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

**Aviso Legal**: Este programa destina-se apenas a fins educacionais. Respeite os direitos autorais e utilize-o com responsabilidade.
