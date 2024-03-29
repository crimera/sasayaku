from datetime import timedelta
from utils import embed
from os import path, getcwd

from faster_whisper import WhisperModel

from abc import ABC, abstractmethod

import whisper
from whisper.utils import (
    get_writer
)


class Model(ABC):
    def __init__(self, model_path, task: str = "translate", device: str = "cpu", compute_type: str = "int8", beam_size: int = 5, vad_filter: bool = False):
        self.model_path = model_path
        self.device = device
        self.compute_type = compute_type
        self.task = task
        self.beam_size = beam_size
        self.vad_filter = vad_filter


class Whisper(Model):
    def __call__(self, filename: str):
        model = whisper.load_model(self.model_path)

        writer = get_writer("srt", "")
        result = model.transcribe(filename, task=self.task)
        writer(result, filename)


class FasterWhisper(Model):
    def __call__(self, filename: str):
        model = WhisperModel(
            self.model_path, device=self.device, compute_type=self.compute_type)

        segments, info = model.transcribe(
            filename, beam_size=self.beam_size, task=self.task, vad_filter=self.vad_filter
        )

        print("Detected language '%s' with probability %f" %
              (info.language, info.language_probability))

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

        with open(filename.rsplit(".", 1)[0]+".srt", 'w') as f:
            print("executed")
            f.write("".join(lines))


def transcribe_and_embed(model: Model, filename: str, thumbnail: str, output_path: str = getcwd()):
    srt_filename = filename.rsplit(".", 1)[0]+".srt"
    output_filename = filename.rsplit(".", 1)[0]+".mkv"

    model(filename)

    embed(filename, srt_filename, thumbnail, path.join(output_path, output_filename.rsplit("/", 1)[-1]))
