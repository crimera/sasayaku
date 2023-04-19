from yabe import transcribe_and_embed, FasterWhisper, Whisper

transcribe_and_embed(FasterWhisper("../../whisper-large-v2-ct2"), "sample/guraclip.opus")
