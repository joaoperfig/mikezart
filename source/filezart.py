from pydub import AudioSegment
import glob
import os
import pickle
import shutil


class instrument:
    def __init__(self, name):
        self._name = name
        self._type = ""                                                         # melodic percussion
        self._nclt = ""                                                         # name_octave octave_name
        self._case = ""                                                         # lower upper
        self._bmsp = ""                                                         # sharp bemol esse
        self._dir1 = ""
        self._dir2 = ""
        self._dvol = 0
        self._dpan = 0
        self._noteslist = ()
        
        self._base = ""                                                         # base note name for modulation
        self._rang = ""                                                         # modulation range

    def __repr__(self):
        return "!"+self._name+"!"

    def getNoteNames(self):                                                     #return list of names of notes in audio file
        if self._type == "modulation":
            raise ValueError("Cannot get notenames of modulation instrument")
        if self._type == "percussion":
            return ("C0", "Db0", "D0", "Eb0", "E0", "F0", "Gb0", "G0", "Ab0", "A0", "Bb0", "B0")
        files = glob.glob("../resources/" + self._dir1 + "*" + self._dir2)
        notenames = ()
        for i in files:
            notename = i[len("../resources/") + len(self._dir1):][:-len(self._dir2)]
            notenames = notenames + (notename,)
        return notenames

    def getAudio(self, formatedName):
        if self._type == "modulation":
            print("../resources/"+self._dir1)
            noteaudio = AudioSegment.from_file("../resources/"+self._dir1)
            noteaudio = noteaudio.pan(self._dpan) + self._dvol
            return noteaudio            
        if self._type == "percussion":
            noteaudio = AudioSegment.from_file("../resources/"+self._dir1)
            noteaudio = noteaudio.pan(self._dpan) + self._dvol
            return noteaudio
        print("../resources/"+self._dir1 + formatedName + self._dir2)
        noteaudio = AudioSegment.from_file("../resources/"+self._dir1 + formatedName + self._dir2)
        noteaudio = noteaudio.pan(self._dpan) + self._dvol
        return noteaudio

def palNames():  #Return names of existing palettes in /exports/
    files = glob.glob("../exports/*")
    names = ()
    for i in files:
        names = names + (cutafter(i, "exports")[1:],)
    return names

def deletePalette(name):    #Deletes all files related to palette name
    shutil.rmtree("../exports/"+name)
    
def openPal(name): #Returns palette saved under this name
    f = open("../exports/"+name+"/pickle.pi", "rb")
    pal= pickle.load(f)
    f.close()
    return pal

def cutafter(string, find):                                                     #returns string cut after first instance of find. cutafter("43211234", "12") -> "34"
    def aux(s1, s2):
        for i in range(len(s2)):
            if s1[i] != s2[i]:
                return False
        return True
    for i in range(len(string)):
        if string[i] == find[0]:
            if aux(string[i:], find):
                return string[i+len(find):]
    raise ValueError("no find in string")

def getInfo():
    mkzrts = glob.glob("../configuration/*.mkzrt")
    instruments = ()
    for mkzrt in mkzrts:
        instruments = instruments + parceMkzrt(mkzrt)
    return instruments

def getInstrument(name):
    insts = getInfo()
    for inst in insts:
        if inst._name == name:
            return inst
    raise ValueError ("Instrument not found in local mkzrt files: " + name)

def getPack(name):
    return parceMkzrt("../configuration/"+name+".mkzrt")

def listbylines(text):                                                          #returns tuple of separate lines in text
    lista = ()
    currtext = ""
    for i in text+"\0":
        if i in ("\n", "\0"):
            lista = lista + (currtext,)
            currtext = ""
        else:
            currtext = currtext + i
    if currtext != "":
        lista = lista + (currtext,)
    return lista

def parceMkzrt(filename):
    file = open(filename, "r")
    text = file.read()
    file.close()
    while text[-1] == "\n":
        text = text[:-1]
    for i in range(len(text)):
        if text[i] == "%":
            text = text[i+3:]
            break
    instblocks = ()
    while True:
        try:
            rest = cutafter(text, "\n\n")
            instblocks = instblocks + (text[:len(text)-(len(rest)+2)],)
            text = rest
        except ValueError:
            instblocks = instblocks + (text,)
            break
    instlines = ()
    for insttext in instblocks:
        instlines = instlines + (listbylines(insttext),)
    instruments = ()
    for cil in instlines:
        nameline = cil[0]
        cil = cil[1:]
        if nameline[:7] != "<Name> ":
            raise ValueError("Poor mkzrt file: name must be first line!")
        else:
            inst = instrument(nameline[7:])
        for i in cil:
            head = i[:7]
            content = i[7:]
            if head == "<Type> ":
                inst._type = content
            elif head == "<Nclt> ":
                inst._nclt = content
            elif head == "<Case> ":
                inst._case = content
            elif head == "<BmSp> ":
                inst._bmsp = content
            elif head == "<FDir> ":
                if "@" in content:
                    rest = cutafter(content, "@")
                    inst._dir1 = filename[16:-6] + content[:len(content)-(len(rest)+1)]
                    inst._dir2 = rest
                else:
                    inst._dir1 = filename[16:-6] + content
                    inst._dir2 = ""
            elif head == "<DVol> ":
                inst._dvol = eval(content)
            elif head == "<DPan> ":
                inst._dpan = eval(content)
            elif head == "<Base> ":
                inst._base = content
            elif head == "<Rang> ":
                inst._rang = content
            else:
                raise ValueError("Invalid line header: "+head)
        instruments = instruments + (inst,)
    return instruments

def makeFolder(name):
    if not os.path.exists(name):
        os.makedirs(name)

def makeTextFile(directory, content):
    f = open(directory, "w")
    f.write(content)
    f.close()

def pickleObject(directory, content):
    f =  open(directory, "wb")
    pickle.dump(content,f )
    f.close()

def unPickle(directory):
    f = open( directory, "rb" )
    data = pickle.load(f)
    f.close()
    return data

def unPPOfSong(name):
    return unPickle("exports/song_"+name+"/pickle.pi")

def readText(filename):
    f=open(filename, "r")
    text = f.read()
    f.close()
    return text

def readLines(filename):
    f=open(filename, "r")
    lines = f.readlines()
    f.close()
    return lines

def getMarkov():
    return unPickle("../configuration/data.mrkv")

def saveMarkov(markov):
    pickleObject("../configuration/data.mrkv", markov)
