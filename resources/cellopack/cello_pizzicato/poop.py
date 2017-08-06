import glob
import shutil
from pydub import AudioSegment

def poo():
    for file in glob.glob("*"):
        if file != "poop.py":
            shutil.move(file, file[6:])
            
def poo2():
    for file in glob.glob("*"):
        if file != "poop.py":
            a = AudioSegment.from_file(file)
            a.export(file[:-4]+".mp3", format = "mp3")