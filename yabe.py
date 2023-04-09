from datetime import timedelta

import ffmpeg
from faster_whisper import WhisperModel

# @title Download and transcribe automatically saving to gdrive
url = "https://raw.kiko-play-niptan.one/media/download/daily/2023-04-04/RJ01032675/mp3%5B320kbps%5D/01_%E6%9C%AC%E7%B7%A8/01_%E3%82%88%E3%81%86%E3%81%93%E3%81%9D%E3%82%84%E3%81%8A%E3%82%88%E3%82%8D%E6%B8%A9%E6%B3%89%E9%83%B7%E3%81%B8%EF%BD%9E%E5%A4%A7%E5%A5%BD%E3%81%8D%E3%81%AA%E3%81%82%E3%81%AA%E3%81%9F%E3%81%AB%E3%81%94%E6%81%A9%E8%BF%94%E3%81%97%E3%81%97%E3%81%BE%E3%81%99%EF%BD%9E.mp3"  # @param {type:"string"}


class VideoTranscriber:
    def __init__(self, model_path: str):
        self.model_path: str = model_path

    def embed(self, filename, subs: str, output: str):
        (
            ffmpeg
            .input(str(filename))
            .output(output, format='mp4', vcodec='copy', acodec='copy', scodec='mov_text',
                    metadata='language=jpn')
            .global_args("-f", "srt", "-i", subs)
            .run()
        )

    def transcribe_and_embed(self, filename):
        srt_filename = f"{filename}.srt"
        output_filename = f"{filename}.mp4"

        # Generate translation
        # !whisper --model=large-v2 --initial_prompt="$filename" --task=translate "$filename"
        # model_path = "whisper-large-v2-ct2/"
        model_path = self.model_path

        # Run on GPU with FP16
        # model = WhisperModel(model_path, device="cuda", compute_type="float16")
        # fp 32
        # model = WhisperModel(model_path, device="cuda", compute_type="float32")
        # or run on GPU with INT8
        # model = WhisperModel(model_path, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        model = WhisperModel(model_path, device="cpu", compute_type="int8")

        # lowered the beam, so it will be faster testing it on my laptop, but originally it should be 4 on colab also
        # made temperature 0
        segments, info = model.transcribe(
            filename, beam_size=1, best_of=1, temperature=0, task="translate", vad_filter=True
        )

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        def time(seconds):
            tdelta = timedelta(seconds=seconds)
            hours, rem = divmod(tdelta.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

        # is actually srt just to lazy to change all proceeding srt's are vtt.
        lines = []

        for i, segment in enumerate(segments):
            start = time(segment.start)
            end = time(segment.end)
            text = segment.text.lstrip()
            srt_line = f"\n{i + 1}\n{start},000 --> {end},000\n{text}\n"

            print(srt_line)
            lines.append(srt_line)

        with open(srt_filename, 'w') as f:
            print("executed")
            f.write("".join(lines))

        # Embed the subtitle into the video
        self.embed(filename, srt_filename, output_filename)
