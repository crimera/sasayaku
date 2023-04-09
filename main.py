import yabe
import asmrone
import shutil

transcriber = yabe.VideoTranscriber("../../whisper-large-v2-ct2/")
drivepath = "/content/drive/MyDrive/VoiceWorks"

url = "https://asmr.one/work/RJ01028088?path=%5B%2202_mp3%22%5D#work-tree"

directory = asmrone.getDir(url)
code = asmrone.getCode(url)
tree = asmrone.getWork(code)
links = asmrone.getTrackUrls(directory, tree)
for link in links:
    print(link['title'])
    print(link['mediaDownloadUrl'])
    transcriber.transcribeAndEmbded(link['mediaDownloadUrl'])
    shutil.move(transcriber.outputfilename, drivepath)
    shutil.move(transcriber.vttfilename, drivepath)
