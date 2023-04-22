import asmrone
from utils import download

# url="https://raw.kiko-play-niptan.one/media/download/hvdb/600-699/RJ113242/2%20%E3%83%9C%E3%82%A4%E3%82%B9%E3%83%89%E3%83%A9%E3%83%9E/1%20%E7%AC%AC%E4%B8%80%E7%AB%A0.mp3"

thumbnail = asmrone.get_thumbnail("113242")
print(thumbnail)

download(thumbnail)