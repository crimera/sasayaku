from datetime import timedelta
from utils import embed

from faster_whisper import WhisperModel

import whisper
from whisper.utils import (
    get_writer
)

class Model():
    def __init__(self, model_path):
        self.model_path = model_path

    def transcribe(self):
        pass 

class Whisper(Model):
    def transcribe(self, filename): 
        model = whisper.load_model(self.model_path)
        
        writer = get_writer("srt", "")
        result = model.transcribe(filename, task="translate")
        writer(result, filename)

class FasterWhisper(Model):
    def __init__(self, model_path, device="cpu", compute_type="int8"):
        super().__init__(model_path)
        self.device = device
        self.compute_type = compute_type

    def transcribe(self, filename: str):
        model = WhisperModel(self.model_path, device=self.device, compute_type=self.compute_type);

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
