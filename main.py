import argparse
from yabe import transcribe_and_embed, FasterWhisper
import asmrone
import shutil
import utils
import os

def move(src: dict, out: str, makedir: bool):
    if not os.path.exists(out):
        if not makedir:
            print("folder does not exist")
            return

        os.mkdir(out)
    else: 
        print("already exist")
    
    for file in src:
        shutil.move(file, out)

def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", help="name or path of the Whisper model to use")
    parser.add_argument("--device", default="cuda", choices=["cpu", "cuda"], help="the device to use for transcribeing")
    parser.add_argument("--compute_type", default="float32" ,choices=["float32", "float16", "int8_float16", "int8"], help="The compute type used")
    parser.add_argument("url", type=str, help="url to download")

    args = parser.parse_args()
    url = args.url
    model = args.model
    device = args.device
    compute_type = args.compute_type

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
        if not link['title'].endswith(("mp3", "wav", "opus", "flac")):
            print("not a valid audio file")
            continue

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
            transcribe_and_embed(FasterWhisper(model, device=device, compute_type=compute_type), filename)

        # Move files
        move([output_filename, output_subs_filename], output_path, True)

if __name__ == "__main__":
    cli()
