import yabe
import asmrone
import shutil
import utils

transcriber = VideoTranscriber("whisper-large-v2-ct2/")
drivepath = "/content/drive/MyDrive/VoiceWorks"

print("getting tracks...")
directory = get_dir(url)
code = get_code(url)
tree = get_work(code)
links = get_track_urls(directory, tree)

print(f"found: {len(links)} tracks")

for index, link in enumerate(links):
    print(f"Downloading [{index+1}/{len(links)}]")
    
    if 'mediaDownloadUrl' not in link.keys():
      print("is a folder")
      continue
    
    track_link = link['mediaDownloadUrl']
    print(link['title'])
    print(track_link)

    # download
    filename = download(track_link)

    # transcribe
    print("transcribing...")
    transcriber.transcribe_and_embed(filename)
    try:
        shutil.move(f"{filename}.mp4", drivepath)
        shutil.move(f"{filename}.srt", drivepath)
    except Exception:
        print("File already exists")
