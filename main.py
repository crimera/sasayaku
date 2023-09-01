import argparse
from yabe import transcribe_and_embed, FasterWhisper
import asmrone
import yt_dlp
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

def asmrone_link(model: FasterWhisper, url: str, save_thumbnail: bool, drivepath: str):
    print("getting tracks...")
    directory = asmrone.get_dir(url)
    code = asmrone.get_code(url)
    tree = asmrone.get_work(code)
    links = asmrone.get_track_urls(directory, tree)
    thumbnail = asmrone.get_thumbnail(code) if save_thumbnail == True else ""

    output_path = f"{drivepath}/RJ{code}/"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if save_thumbnail==True:
        print("saving thumbnail")
        utils.download(thumbnail, output_path)

    print(f"found: {len(links)} tracks")

    for index, link in enumerate(links):
        filename = link['title']
        output_filename = filename.rsplit(".", 1)[0]+".mkv"
        # output_subs_filename = filename.rsplit(".", 1)[0]+".srt"

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
        utils.download(track_link)

        # transcribe
        if not os.path.exists(output_path+output_filename):
            print("transcribing...")
            thumb_path = output_path+utils.get_filename(thumbnail)
            transcribe_and_embed(model, filename, thumb_path, output_path)

        else:
            print(f"{output_filename} found, not transcribing")

filename = "" 
def yt_link(model: FasterWhisper, url: str, drivepath: str):    
    global filename
    def my_hook(d):
        if d['status'] == 'finished':
            global filename
            filename = d.get('info_dict').get('_filename')
            print('Done downloading, now post-processing ...')
    
    
    ydl_opts = {
            'format': 'bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
            }],
            "progress_hooks": [my_hook]  # here's the function we just defined
        }
 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error = ydl.download(url)
    
    filename = filename.rsplit(".", 1)[0]+".opus"    
    transcribe_and_embed(model, filename)

def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument("--model", help="whisper model to use")
    # parser.add_argument("--model_size", default="small", help="the model to use when using the original whisper inference")
    parser.add_argument("--model_path", help="name or path of the Whisper model to use")
    parser.add_argument("--save_thumbnail", default=False, action=argparse.BooleanOptionalAction, help="downloads the thumbnail of the work")
    parser.add_argument("--vad_filter", default=False, action=argparse.BooleanOptionalAction, help="applies vad filter")
    parser.add_argument("--task", choices=["transcribe", "translate"], help="task for the transciber")
    parser.add_argument("--device", default="cuda", choices=["cpu", "cuda"], help="the device to use for transcribeing")
    parser.add_argument("--compute_type", default="float32" ,choices=["float32", "float16", "int8_float16", "int8"], help="The compute type used")
    parser.add_argument("--output", type=str, help="The output path")
    parser.add_argument("url", type=str, help="url to download")

    args = parser.parse_args()
    # _model = args.model
    # model_size = args.model_size
    task = args.task
    url: str = args.url
    model_path = args.model_path
    device = args.device
    compute_type = args.compute_type
    drivepath = args.output
    save_thumbnail = args.save_thumbnail
    vad_filter = args.vad_filter 

    model = FasterWhisper(
        model_path=model_path, 
        task=task,device=device, 
        compute_type=compute_type, 
        vad_filter=vad_filter
    )

    if url.startswith("https://asmr.one"):
        asmrone_link(model, url, save_thumbnail, drivepath) 
    else:        
        yt_link(model, url, drivepath)

if __name__ == "__main__":
    cli()
