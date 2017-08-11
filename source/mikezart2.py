from musictheory import palette
from random import random
from pydub import AudioSegment
from pydub.playback import play
import glob
import operator
import naming
import filezart
import copy
from filezart import instrument
import musictheory

# rselect RandomSelect returns random element of list
def rselect  (lista):
    dicti = {}
    for i in lista:
        dicti[i] = 1
    return wselect(dicti)

# wselect WeightedSelect returns element of dictionary based on dict weights {element:weight}
def wselect(dicti):
    total=0
    for i in list(dicti):
        total = total + dicti[i]
    indice = total*random()
    for i in list(dicti):
        if dicti[i]>=indice:
            return i
        indice = indice - dicti[i]
    raise ValueError ("something went wrong")

# Make random song with selected instruments
def palFromInsts(cinsts, sminsts, lminsts, pinsts):
    
    scale = musictheory.scale7()
    progsize = rselect((2,3,4,5,6))
    progcount = rselect((1,2,3,4,5))
    csize = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
    bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})
    name = naming.name()
    print("making",name)
    
    palett = musictheory.palette(scale, progsize, progcount, csize)
    palett.autoProgs()
    themes = (palett._n1, palett._n2, palett._bg, palett._ch, palett._ge)
    
    for inst in cinsts:
        for them in themes:
            centre = rselect(musictheory.listNotes(inst))
            ncount = wselect(musictheory.chordicCWeights())
            them.addVoice(inst, centre, "chordic", ncount)
            
    for inst in sminsts:
        for them in themes:
            centre = rselect(musictheory.listNotes(inst))
            ncount = wselect(musictheory.smelodicCWeights())
            them.addVoice(inst, centre, "smelodic", ncount)
            
    for inst in lminsts:
        for them in themes:
            centre = rselect(musictheory.listNotes(inst))
            ncount = wselect(musictheory.lmelodicCWeights())
            them.addVoice(inst, centre, "lmelodic", ncount)
            
    for inst in pinsts:
        for them in themes:
            centre = rselect(musictheory.listNotes(inst))
            ncount = wselect(musictheory.percussionCWeights())
            them.addVoice(inst, centre, "percussion", ncount)
            
    filezart.makeFolder("../exports/song_" + name)
    palett.infoToFolder(bpm, "../exports/song_" + name)
    
    print("done with", name)
            
    return palett




#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def pooptest1():
    cinsts = (filezart.getInstrument("Vibraphone_bow"), filezart.getInstrument("Vibraphone_dampen"),filezart.getInstrument("Piano_original"),)
    pinsts =  ()#(filezart.getInstrument("Wood_Pipe_h10"),)
    lminsts = ()
    sminsts = ()#(filezart.getInstrument("Piano_original"),)
    return palFromInsts(cinsts, sminsts, lminsts, pinsts)

def pooptest2():
    cinsts = (filezart.getInstrument("Cello_pianissimo_arco_normal_05"),filezart.getInstrument("Piano_original"),)
    pinsts =  ()#(filezart.getInstrument("Wood_Pipe_h10"),)
    lminsts = ()
    sminsts = (filezart.getInstrument("Vibraphone_dampen"),)
    return palFromInsts(cinsts, sminsts, lminsts, pinsts)

print("This is just a test \nA palette file will appear on mikezart/exports,\ncheck out how the themes sound on each folder")
pooptest2()
print("This is just a test \nA palette file will appear on mikezart/exports,\ncheck out how the themes sound on each folder")