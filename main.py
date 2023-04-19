from yabe import transcribe_and_embed, FasterWhisper
import asmrone
import shutil
import utils
import os

def move(src: dict, out: str, makedir: bool):
    if not os.path.exists(out):
        if not mkdir:
            print("folder does not exist")
            return

        os.mkdir(out)
    else: 
        print("already exist")
    
    for file in src:
        shutil.move(file, out)

drivepath = "/home/gura/AI/whisper/projects/autotranscribe"

print("getting tracks...")
directory = asmrone.get_dir(url)
code = asmrone.get_code(url)
tree = asmrone.get_work(code)
links = asmrone.get_track_urls(directory, tree)

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
    filename = utils.download(track_link)
    output_filename = f"{filename}.mp4"
    output_subs_filename = f"{filename}.srt"

    # transcribe
    print("transcribing...")
    if not os.path.exists(output_filename):
      print("file already exists")
      transcribe_and_embed(FasterWhisper("../../whisper-large-v2-ct2/"), filename)

    # Move files
    move([output_filename, output_subs_filename], output_path, True)
