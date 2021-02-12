import youtube_dl
import os

file = './song.mp3'

def ydl(url) :
    if os.path.isfile(file):  # song.mp3파일이 존재하면
        os.remove(file)  # 파일 삭제

    ydl_opts = {  # 다운로드 옵션
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.mp3',  # 파일 이름
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # 다운로드