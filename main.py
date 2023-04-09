import yabe
import asmrone
import shutil
import utils
import os

transcriber = VideoTranscriber("whisper-large-v2-ct2/")
drivepath = "/content/drive/MyDrive/VoiceWorks"

print("getting tracks...")
directory = get_dir(url)
code = get_code(url)
tree = get_work(code)
links = get_track_urls(directory, tree)

output_path = f"{drivepath}/RJ{code}/"
if not os.path.exists(output_path):
    os.mkdir(output_path)

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
    output_filename = f"{filename}.mp4"
    output_subs_filename = f"{filename}.srt"

    # transcribe
    print("transcribing...")
    if not os.path.exists(output_filename):
      print("file already exists")
      transcriber.transcribe_and_embed(filename)

    if not os.path.exists(f"{output_path}/{output_filename}"):
        shutil.move(output_filename, output_path)
        shutil.move(output_subs_filename, output_path)
    else:
        print("already exists on drive")
