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
import markovzart2

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
def palFromInsts(cinsts, sminsts, lminsts, pinsts, ginsts, name=None):
    if name == None:
        name = naming.name()
    scale = musictheory.scale7()
    progsize = rselect((2,3,4,5,6))
    progcount = rselect((1,2,3,4,5))
    csize = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
    bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})
    print("making",name)
    
    palett = musictheory.palette(scale, progsize, progcount, csize)
    palett._bpm = bpm
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
            
    for inst in ginsts:
        for them in themes:
            centre = rselect(musictheory.listNotes(inst))
            ncount = wselect(musictheory.genericCWeights())
            them.addVoice(inst, centre, "generic", ncount)    
            
    for t in themes:
        t.shuffleSort()
            
    filezart.makeFolder("../exports/song_" + name)
    palett.infoToFolder(bpm, "../exports/song_" + name)
    
    #play(palett._n1.previewAudio(bpm))
    #play(palett._n2.previewAudio(bpm))
    #play(palett._bg.previewAudio(bpm))
    #play(palett._ch.previewAudio(bpm))
    
    print("done with", name)
            
    return palett

def testInst(name):
    inst = filezart.getInstrument(name)
    scale = musictheory.scale7()
    progsize = rselect((2,3,4,5,6))
    progcount = rselect((1,2,3,4,5))
    csize = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
    bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})   
    palett = musictheory.palette(scale, progsize, progcount, csize)
    palett._bpm = bpm
    palett.autoProgs()    
    for i in range(2):
        centre = rselect(musictheory.listNotes(inst))
        ncount = wselect(musictheory.chordicCWeights())
        palett._n1.addVoice(inst, centre, "chordic", ncount)    
    play(palett._n1.previewAudio(bpm))


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def pooptest1(name):
    cinsts = (filezart.getInstrument("Vibraphone_bow"), filezart.getInstrument("Vibraphone_dampen"),filezart.getInstrument("Piano_original"),)
    pinsts =  (filezart.getInstrument("Wood_Pipe_h10"),)
    lminsts = ()
    sminsts = (filezart.getInstrument("Piano_original"),)
    ginsts = ()
    return palFromInsts(cinsts, sminsts, lminsts, pinsts, ginsts, name)

def pooptest2(name):
    cinsts = (filezart.getInstrument("Cello_pianissimo_arco_normal_05"),filezart.getInstrument("Piano_original"),)
    pinsts =  (filezart.getInstrument("BassDrum_9"), filezart.getInstrument("Egg_3"))
    lminsts = ()
    sminsts = ()
    ginsts = (filezart.getInstrument("Piano_original"),)
    return palFromInsts(cinsts, sminsts, lminsts, pinsts, ginsts, name)

def rocktest(name):
    cinsts = (rselect((ins("Bass"), ins("Soft_Bass_M"), ins("Snap_Bass_M"))), rselect((ins("Acoustic_Guitar"), ins("Electric_Guitar"), ins("Long_Guitar_2_M"))))
    pinsts =  (rselect(ipack("drumkit")), rselect(ipack("drumkit")), rselect(ipack("drumkit")), rselect(ipack("drumkit")), rselect(ipack("drumkit")))
    lminsts = ()
    sminsts = (rselect((ins("Long_Guitar_3_M"), ins("Short_Guitar_3_M"), ins("Long_Guitar_2_M"))),)
    ginsts = (rselect((ins("Piano_original"), ins("Short_Guitar_3_M"))),)
    return palFromInsts(cinsts, sminsts, lminsts, pinsts, ginsts, name)

def mtest():
    inst = rselect(ipack("churchpiano"))
    scale = musictheory.scale7()
    progsize = rselect((2,3,4,5,6))
    progcount = rselect((1,2,3,4,5))
    csize = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
    bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})   
    palett = musictheory.palette(scale, progsize, progcount, csize)
    palett._bpm = bpm
    palett.autoProgs()    
    centre = rselect(musictheory.listNotes(inst))
    ncount = wselect(musictheory.chordicCWeights())
    palett._n1.addVoice(inst, centre, "chordic", ncount)  
    
    inst = rselect(ipack("guitars"))
    centre = rselect(musictheory.listNotes(inst))
    ncount = wselect(musictheory.chordicCWeights())
    voic = musictheory.voice(inst, centre, scale, "chordic", 0, 0)
    voic.mimic(palett._n1._voices["chordic"][0])
    palett._n1.addVoiceAsIs(voic)      
    
    inst = rselect(ipack("cellopack"))
    centre = rselect(musictheory.listNotes(inst))
    ncount = wselect(musictheory.chordicCWeights())    
    palett._n1.addVoice(inst, centre, "chordic", ncount)  
    
    play(palett._n1.previewAudio(bpm))    
    print(palett._n1._voices["chordic"][0]._cent)
    print(palett._n1._voices["chordic"][1]._cent)

def ins(name):
    return filezart.getInstrument(name)

def ipack(name):
    return filezart.getPack(name)

def ttest():
    name = naming.name()
    pal = rocktest(name)
    struct = markovzart2.makeStruct()
    print(struct)
    print(struct.baseDur(pal, pal._bpm))
    print((struct.baseDur(pal, pal._bpm)/1000)//60,":",(struct.baseDur(pal, pal._bpm)/1000)%60)
    a = struct.songAudio(pal)
    a.export("../exports/fullSongs/song_"+name+".mp3", format = "mp3")
    print(struct)
    print(struct.baseDur(pal, pal._bpm))
    print((struct.baseDur(pal, pal._bpm)/1000)//60,":",(struct.baseDur(pal, pal._bpm)/1000)%60)
    print("Really done with "+name)
    
def adjustTest(pack = None, splay=True):
    if pack == None:
        pack = filezart.getInfo()
    else:
        pack = filezart.getPack(pack)
    for i in pack:
        clip = musictheory.getNote(i, musictheory.listNotes(i)[len(musictheory.listNotes(i))//2])
        dest = -30
        if splay:
            play(clip)
        print("audio:",clip.max_dBFS)
        print("delta:",dest-clip.max_dBFS)
        
def testPack(name):
    for inst in filezart.getPack(name):
        testInst(inst._name)
        





print("Write 'y' to generate a song or the name of a pack or instrument to preview it")
print("'m' for mega generation")
inp = input(">") 
if inp == "y":
    print("This is just a test \nA palette file will appear on mikezart/exports,\ncheck out how the themes sound on each folder")
    ttest()
    print("This is just a test \nA palette file will appear on mikezart/exports,\ncheck out how the themes sound on each folder")
    print("A structure was also generated and a full song is located in /exports/fullSongs")
if inp == "m":
    for i in range(20):
        ttest()
else:
    try:
        testPack(inp)
    except:
        try:
            testInst(inp)
        except:
            raise ValueError("no such instrument or pack: "+inp)