from yabe import transcribe_and_embed, FasterWhisper, Whisper

transcribe_and_embed(Whisper("base.en"), "sample/guraclip.opus")
