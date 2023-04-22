import pycurl
import os
import ffmpeg
import urllib.parse


def download(url, output: str = ""):
    # Create a Curl object
    c = pycurl.Curl()
    # Set the URL of the file to download
    c.setopt(c.URL, url)
    # get the filename
    effective_url = c.getinfo(pycurl.EFFECTIVE_URL)
    filename = os.path.basename(urllib.parse.unquote(urllib.parse.urlsplit(effective_url).path))

    outpath = os.path.join(output, filename)
    if os.path.exists(outpath):
        print(f"{outpath} is already downloaded")
        c.close()
        return

    # Set the name of the output file
    with open(outpath, 'wb') as f:
        # Write the downloaded data to the file
        c.setopt(c.WRITEDATA, f)
        # Perform the request
        c.perform()
        # Close the Curl object
        c.close()

def embed(filename: str, subs: str, output: str):
    # Define input streams
    audio_stream = ffmpeg.input(filename)
    subtitle_stream = ffmpeg.input(subs)

    # Define output stream with parameters
    output_stream = ffmpeg.output(
        audio_stream,
        subtitle_stream,
        output,
        acodec="copy",
        scodec="copy",
        **{"metadata:s:s:0": "language=jpn", "metadata": "title="}
    )

    # Overwrite output file if exists
    output_stream = ffmpeg.overwrite_output(output_stream)

    # Print equivalent ffmpeg command
    print(ffmpeg.compile(output_stream))

    # Run the command
    ffmpeg.run(output_stream)
