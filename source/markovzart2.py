import random
import musictheory
import filezart
import math
from pydub import AudioSegment
from pydub.playback import play

class Part:

    def __init__(self, typ=None, intensity=0, size=0, gen=0, cho=0):
        self._type = typ #"n1", "n2", "bg", "ch", "ge"
        if intensity<0 or gen<0 or cho<0 or size<0 or intensity>1 or size>1 or gen>1 or cho>1:
            raise ValueError ("Invalid Values for Structure Part")
        self._intensity = intensity # [0-1]
        self._size = size # [0-1]
        self._genover = gen # [0-1] overlay of general type lines
        self._chover = cho # [0-1] overlay of chorus type lines

    def __repr__(self):
        return "[" + self._type + "-" + str(self._intensity) + "-" + str(self._size) + "-" + str(self._genover) + "-" + str(self._chover) + "]"

    @classmethod
    def fromString(cls, string): # [n1-0.123-1-0.321-0.2] type, intensity, size, genoverlay, chooverlay
        while string[0] == " ":
            string = string[1:]
        while string[0] == "\n":
            string = string[1:]
        while string[-1] == " ":
            string = string[:-1]
        while string[-1] == "\0":
            string = string[:-1]
        while string[-1] == "\n":
            string = string[:-1]
        if len(string)<8:
            raise ValueError("Invalid Part string: "+string)
        if string[0] == "[" and string[-1] == "]":
            string = string[1:-1]
        else:
            raise ValueError("Invalid Part string: "+string)
        typ = string[:2]
        string = string[3:]
        if not typ in ("n1", "n2", "bg", "ch", "ge"):
            raise ValueError("Invalid Part Type string: "+typ)
        valstrings = str.split(string, "-")
        inten = eval(valstrings[0])
        size = eval(valstrings[1])
        gen = eval(valstrings[2])
        cho = eval(valstrings[3])
        return cls(typ, inten, size, gen, cho)
    
    def getTheme(self, pal):
        if self._type == "n1":
            return pal._n1
        if self._type == "n2":
            return pal._n2
        if self._type == "bg":
            return pal._bg
        if self._type == "ch":
            return pal._ch
        if self._type == "ge":
            return pal._ge
    
    def getAudio(self, pal, bpm):
        base = self.baseDur(pal, bpm)
        total = base + 3000 #extra time for last note to play
        nvoic = math.ceil(self._intensity * self.getTheme(pal).countVoices())
        try:
            ngeno = math.ceil(self._genover * pal._ge.countVoices())
        except:
            ngeno = 0
        try:
            nchoo = math.ceil(self._chover * pal._ch.countVoices())
        except:
            nchoo = 0
        
        sound = AudioSegment.silent(total)
        them = self.getTheme(pal)
        for i in range(nvoic):
            voic = them._sorting[i].getVoice(them)
            print(them._sorting[i].indicationStr(them)) #DEBUG !!
            vsound = voic.partialAudio(self._size, bpm)
            sound = sound.overlay(vsound)
            
        them = pal._ge
        for i in range(ngeno):
            voic = them._sorting[i].getVoice(them)
            print(them._sorting[i].indicationStr(them)) #DEBUG !!
            vsound = voic.partialAudio(self._size, bpm)
            sound = sound.overlay(vsound)        
        
        them = pal._ch
        for i in range(nchoo):
            voic = them._sorting[i].getVoice(them)
            print(them._sorting[i].indicationStr(them)) #DEBUG !!
            vsound = voic.partialAudio(self._size, bpm)
            sound = sound.overlay(vsound)        
            
        return sound
                
    
    def baseDur(self, pal, bpm):                                                #get the base duration of this part of the song
        return self.getTheme(pal).baseDurForStruct(self._size, bpm)


class Structure:

    def __init__(self):
        self._parts = ()

    def add(self, part):
        self._parts = self._parts+(part,)

    def __repr__(self):
        return "@STRUCTURE:" + str(self._parts) 
    
    def baseDur(self, pal, bpm=None):
        if bpm == None:
            bpm = pal._bpm
        curTime = 0
        for p in self._parts:
            curTime = curTime + p.baseDur(pal, bpm)
        return curTime
    
    def songAudio(self, pal, bpm=None):
        if bpm == None:
            bpm = pal._bpm
        total = self.baseDur(pal, bpm) + 3000 # 3 seconds for last note to play
        sound = AudioSegment.silent(total)
        curTime = 0
        for p in self._parts:
            paudio = p.getAudio(pal, bpm)
            sound = sound.overlay(paudio, curTime)
            curTime = curTime + p.baseDur(pal, bpm)
            print("curTime:",curTime)
        return sound
    
# wselect WeightedSelect returns element of dictionary based on dict weights {element:weight}
def wselect(dicti):
    total=0
    for i in list(dicti):
        total = total + dicti[i]
    indice = total*random.random()
    for i in list(dicti):
        if dicti[i]>=indice:
            return i
        indice = indice - dicti[i]
    raise ValueError ("something went wrong")

# rselect RandomSelect returns random element of list
def rselect(lista):
    return random.choice(lista)




def lenweights():
    return {3:1, 4:1, 5:2, 6:3, 7:4, 8:3, 9:2, 10:1, 11:1}


def stweights():
    return {"n1":5, "n2":4, "ch":2, "bg":1}

def n1weights():
    return {"n1":4, "n2":2, "ch":3, "bg":1}

def n2weights():
    return {"n1":2, "n2":3, "ch":4, "bg":2}

def chweights():
    return {"n1":2, "n2":1, "ch":4, "bg":1}

def bgweights():
    return {"n1":1, "n2":1, "ch":20, "bg":8}

def typeSequence(size):
    last = wselect(stweights())
    sequence=(last,)
    while len(sequence)<size:
        if last == "n1":
            last = wselect(n1weights())
        elif last == "n2":
            last = wselect(n2weights())
        elif last == "ch":
            last = wselect(chweights())
        elif last == "bg":
            last = wselect(bgweights())
        sequence = sequence + (last,)
    return sequence


def siweights():
    return {0.1:1, 0.2:2, 0.3:4, 0.4:5, 0.5:5, 0.6:4, 0.7:3, 0.8:2, 0.9:1}

def deltaweights():
    return {-0.3:1, -0.2:1, -0.1:1, 0:5, 0.1:3, 0.2:2, 0.3:2}

def intensitySequence(size):
    val = wselect(siweights())
    sequence = (val,)
    while len(sequence)<size:
        val = val + wselect(deltaweights())
        if val<0.1:
            val = 0.1
        if val>1:
            val = 1
        sequence = sequence + (val,)
    return sequence


def soweights():
    return {0:6, 0.1:2, 0.2:1}

def deltoweights():
    return {-0.2:1, -0.1:1, 0:8, 0.1:2, 0.2:2}

def overlaySequence(size):
    val = wselect(soweights())
    sequence = (val,)
    while len(sequence)<size:
        val = val + wselect(deltoweights())
        if val<0.1:
            val = 0.1
        if val>1:
            val = 1
        sequence = sequence + (val,)
    return sequence


def ssweights():
    return {0.2:1, 0.4:1, 0.6:1, 0.8:1, 1:16}

def sizeSequence(size):
    sequence = ()
    while len(sequence)<size:
        sequence = sequence + (wselect(ssweights()),)
    return sequence


def makeStruct(size = None):
    if size == None:
        size = wselect(lenweights())
    types = typeSequence(size)
    inten = intensitySequence(size)
    sizes = sizeSequence(size)
    overl = overlaySequence(size)
    return joinSeqs(types, inten, sizes, overl)

def joinSeqs(types, inten, sizes, overl):
    struct = Structure()
    for i in range(len(types)):
        if types[i]=="bg":
            string = "["+types[i]+"-"+str(inten[i])+"-"+str(sizes[i])+"-"+"0"+"-"+str(overl[i])+"]" # If its a bridge it has chord overlay
            pt = Part.fromString(string)
            struct.add(pt)
        else:
            string = "["+types[i]+"-"+str(inten[i])+"-"+str(sizes[i])+"-"+str(overl[i])+"-"+"0"+"]" # Else it has gen overlay
            pt = Part.fromString(string)
            struct.add(pt)
    return struct


def pooptest():
    for i in range(30):
        print(makeStruct())
        

