from datetime import timedelta
from utils import embed

import ffmpeg
from abc import ABC,abstractmethod
from faster_whisper import WhisperModel

import whisper

class Model(ABC):
    def __init__(self, model_path):
        self.model_path = model_path

    @abstractmethod
    def transcribe(self):
        pass 

class Whisper(Model):
    def transcribe(self, filename): 
        model = whisper.load_model(self.model_path)
        result = model.transcribe(filename)
        print(result.srt)

class FasterWhisper(Model):
    def transcribe(self, filename: str, device="cpu", compute_type="int8"):
        model = WhisperModel(self.model_path, device=device, compute_type=compute_type);

        segments, info = model.transcribe(
            filename, beam_size=1, best_of=1, temperature=0, task="translate", vad_filter=True
        )

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        def time(seconds):
            tdelta = timedelta(seconds=seconds)
            hours, rem = divmod(tdelta.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

        lines = []

        for i, segment in enumerate(segments):
            start = time(segment.start)
            end = time(segment.end)
            text = segment.text.lstrip()
            srt_line = f"\n{i + 1}\n{start},000 --> {end},000\n{text}\n"

            print(srt_line)
            lines.append(srt_line)

        with open(f"{filename}.srt", 'w') as f:
            print("executed")
            f.write("".join(lines))

def transcribe_and_embed(model: Model, filename: str):
    srt_filename = f"{filename}.srt"
    output_filename = f"{filename}.mkv"

    model.transcribe(filename)

    embed(filename, srt_filename, output_filename)
