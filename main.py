import argparse
from yabe import Whisper, transcribe_and_embed, FasterWhisper
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
    parser.add_argument("--model", help="whisper model to use")
    parser.add_argument("--task", default="translate", choices=["translate", "transcribe"], help="Either you translate or just transcribe the audio")
    parser.add_argument("--model_path", help="name or path of the Whisper model to use")
    parser.add_argument("--model_size", default="small", help="the model to use when using the original whisper inference")
    parser.add_argument("--device", default="cuda", choices=["cpu", "cuda"], help="the device to use for transcribeing")
    parser.add_argument("--compute_type", default="float32" ,choices=["float32", "float16", "int8_float16", "int8"], help="The compute type used")
    parser.add_argument("--output", type=str, help="The output path")
    parser.add_argument("url", type=str, help="url to download")

    args = parser.parse_args()
    _model = args.model
    task = args.task
    url = args.url
    model_path = args.model_path
    model_size = args.model_size
    device = args.device
    compute_type = args.compute_type
    drivepath = args.output

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
        filename = link['title']
        output_filename = filename.rsplit(".", 1)[0]+".mkv"
        output_subs_filename = filename.rsplit(".", 1)[0]+".srt"

        if not filename.endswith(("mp3", "wav", "opus", "flac")):
            print("not a valid audio file")
            continue

        print(f"Downloading [{index+1}/{len(links)}]")
    
        if 'mediaDownloadUrl' not in link.keys():
            print("is a folder")
            continue
    
        track_link = link['mediaDownloadUrl']
        print(filename)
        print(track_link)

        # download
        if not os.path.exists(link['title']):
            utils.download(track_link)
        else:
            print("file is already downloaded")

        # transcribe
        if not os.path.exists(output_path+output_filename):
            print("transcribing...")
            model = Whisper(model_size, task) if _model == "whisper" else FasterWhisper(model_path=model_path, device=device, compute_type=compute_type)
            
            transcribe_and_embed(model, filename)
            # Move files
            move([output_filename, output_subs_filename], output_path, True)
        else:
            print(f"{output_filename} found, not transcribing") 

if __name__ == "__main__":
    cli()
