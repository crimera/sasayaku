import yabe
import asmrone
import shutil
import utils

transcriber = yabe.VideoTranscriber("../../whisper-large-v2-ct2/")
drivepath = "/content/drive/MyDrive/VoiceWorks"

url = "https://asmr.one/work/RJ01026607?path=%5B%22%E6%9C%AC%E7%B7%A8%22,%22mp3%22,%22%E6%81%8B%E3%82%92%E3%81%97%E3%81%9F%E3%81%82%E3%81%AA%E3%81%9F%E3%81%B8%E3%80%82%22,%22%E3%81%AA%E3%82%86%E3%81%AE%E6%B0%97%E6%8C%81%E3%81%A1%E3%82%92%E5%8F%97%E3%81%91%E5%85%A5%E3%82%8C%E3%82%8B%E3%80%82%22,%22%E3%82%B7%E3%83%81%E3%83%A5%E3%82%A8%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%9C%E3%82%A4%E3%82%B9%22%5D#work-tree"

print("getting tracks...")
directory = asmrone.get_dir(url)
code = asmrone.get_code(url)
tree = asmrone.get_work(code)
links = asmrone.get_track_urls(directory, tree)

print(f"found: {len(links)} tracks")

for index, link in enumerate(links):
    print(f"Downloading [{index+1}/{len(links)}]")

    track_link = link['mediaDownloadUrl']
    print(link['title'])
    print(track_link)

    # download
    filename = utils.download(track_link)

    # transcribe
    print("transcribing...")
    transcriber.transcribe_and_embed(filename)
    shutil.move(f"{filename}.mp4", drivepath)
    shutil.move(f"{filename}.srt", drivepath)