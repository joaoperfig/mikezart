import musictheory
import random
import operator
import pianoprinter

# rselect RandomSelect returns random element of list
def rselect(lista):
    return random.choice(lista)


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



def mainMenu():
    print("\nWelcome to the MikezarIO music creation interface (art by Forrest Cook & Alexander Craxton)")
    print("      ________________________________    \n     /    o   oooo ooo oooo   o o o  /\    \n    /    oo  ooo  oo  oooo   o o o  / /    \n   /    _________________________  / /     \n  / // / // /// // /// // /// / / / /      \n /___ //////////////////////////_/ /       \n \____\________________________\_\/  \n")
    while True:
        print("Pp - Create a Palette")
        print("Ee - Edit a Palette")
        print("Ss - Create a Structure")
        print("Cc - Create a Song from a Palette and a Structure")
        print("Qq - Quit")
        
        inp = input(">")
        if inp in "Pp":
            paletteMenu()
        
        elif inp in "Qq":
            return

    
def bpmMenu():
    while True:
        print("Please input the number of beats per minute for this Palette (write G or g for random):")
        bpmt = input(">")
        if bpmt in "Gg":
            bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})
        else:
            bpm = eval(bpmt)
        while True:
            print(str(bpm) + " beats per minute. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return bpm
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewbpm(bpm)

def csizeMenu():
    while True:
        print("Please input the number of beats in a chunk for this Palette (write G or g for random):")
        ct = input(">")
        if ct in "Gg":
            cs = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
        else:
            cs = eval(ct)
        while True:
            print(str(cs) + " (x4 quarter) beats in a chunk. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return cs
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewcs(cs)
                
def psizeMenu():
    while True:
        print("Please input the number of chunks in a progression for this Palette (write G or g for random):")
        pt = input(">")
        if pt in "Gg":
            ps = rselect((2,3,4,5,6))
        else:
            ps = eval(pt)
        while True:
            print(str(ps) + " chunks in a progression. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return ps
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewps(ps)
    
def progcMenu():
    while True:
        print("Please input the number of progressions in a voice for this Palette (write G or g for random):")
        pt = input(">")
        if pt in "Gg":
            pc = rselect((2,3,4,5,6))
        else:
            pc = eval(pt)
        while True:
            print(str(pc) + " progressions in a voice. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return pc
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewpc(pc)
    
def scaleMenu():
    while True:
        print("Please input the list of 7 notes in the Scale (ex: 'C Ds E ...'), a smaller list to autocomplete, or write G or g for random:")
        scalet = input(">")
        if scalet in "Gg":
            scale = musictheory.scale7()
        else:
            notenames = str.split(scalet, " ")
            notes = ()
            for i in range(len(notenames)):
                if len(notenames[i]) != 0:
                    notes = notes + (musictheory.mnote.fromName(notenames[i] + "0"),)
            scale = musictheory.scale7(notes)
        while True:
            print ("Your scale: "+str(scale)[2:-2])
            pianoprinter.octoPrint(scale._notes)
            print("Chords |Short  |Normal |Large  ")
            print("Minor  |" + str(len(scale.getChords("minor", "short"))) + "      |" + str(len(scale.getChords("minor", "normal"))) + "      |" + str(len(scale.getChords("minor", "large"))) + "      ")
            print("Weird  |" + str(len(scale.getChords("weird", "short"))) + "      |" + str(len(scale.getChords("weird", "normal"))) + "      |" + str(len(scale.getChords("weird", "large"))) + "      ")
            print("Major  |" + str(len(scale.getChords("major", "short"))) + "      |" + str(len(scale.getChords("major", "normal"))) + "      |" + str(len(scale.getChords("major", "large"))) + "      ")
            print()
            print ("Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return scale
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewscale(scale)
            
def paletteMenu():
    while True:
        print("Starting Palette creation:")
        bpm = bpmMenu()
        csize = csizeMenu()
        progsize = psizeMenu()
        progcount = progcMenu()
        scale = scaleMenu()
        pal = musictheory.palette(scale, progsize, progcount, csize)
        print("Palette created, Accept? Yy Nn")
        inp = input(">")
            if inp in "Yy":
                name = nameMenu()
                paletteEdit(pal, name)
            elif inp in "Nn":
            
mainMenu()
