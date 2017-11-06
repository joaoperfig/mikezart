from musictheory import *
import musictheory
import random
import operator
import pianoprinter
import filezart
from pydub.playback import play
from musictheory import sidePlay
import markovzart2

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

def usrinp(acceptEmpty = False):
    while True:
        try:
            inp = input(">")
        except:
            raise ValueError("Terminated by user!")
        if acceptEmpty == True:
            print("")
            return inp
        elif inp != "":
            print("")
            return inp

def mainMenu():
    print("\nWelcome to the MikezarIO music creation interface (art by Forrest Cook & Alexander Craxton)")
    print("      ________________________________    \n     /    o   oooo ooo oooo   o o o  /\    \n    /    oo  ooo  oo  oooo   o o o  / /    \n   /    _________________________  / /     \n  / // / // /// // /// // /// / / / /      \n /___ //////////////////////////_/ /       \n \____\________________________\_\/  \n")
    while True:
        print("Pp - Create a Palette")
        print("Ee - Edit a Palette")
        print("Ss - Create a Structure")
        print("Cc - Create a Song from a Palette and a Structure")    #UNDEFINED OPTIONS
        print("Qq - Quit")
        
        inp = usrinp()
        if inp in "Pp":
            paletteMenu()
        
        elif inp in "Ee":
            res = openPalettMenu()
            if res != None:
                pal = res[0]
                name = res[1]
                paletteEdit(pal, name)
        
        elif inp in "Qq":
            return

def openPalettMenu(): # Open existing palette, returns None if failed
    print("Opening Palette from file")
    while True:
        pals = existingPalNames()
        print("Existing Palettes (all files in /exports/):")
        for paln in pals:
            print ("    "+paln)
        print("Please type the name of the palette you want to open or Qq to quit")
        inp = usrinp()
        if inp in "Qq":
            return None
        else:
            for paln in pals:
                if inp == paln:
                    pal = getPalette(paln)
                    return (pal, paln)
                
def existingPalNames():
    return filezart.palNames()

def getPalette(name):
    return filezart.openPal(name)                
    
def bpmMenu():
    while True:
        print("Please input the number of beats per minute for this Palette (write G or g for random):")
        bpmt = usrinp()
        if bpmt in "Gg":
            bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})
        else:
            bpm = eval(bpmt)
        while True:
            print(str(bpm) + " beats per minute. Accept? (Yy, Nn, Pp(preview)):")
            inp = usrinp()
            if inp in "Yy":
                return bpm
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewbpm(bpm)
                
def previewbpm(bpm):
    c = musictheory.chunk(5)
    ins = filezart.getInstrument("Drum_Snare")
    for i in c.wholes():
        c.add(i, mnote.fromName("C0"))
    sidePlay(c.getAudio(ins, bpm))
    
def csizeMenu():
    while True:
        print("Please input the number of beats in a chunk for this Palette (write G or g for random):")
        ct = usrinp()
        if ct in "Gg":
            cs = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
        else:
            cs = eval(ct)
        while True:
            print(str(cs) + " (x4 quarter) beats in a chunk. Accept? (Yy, Nn, Pp(preview)):")
            inp = usrinp()
            if inp in "Yy":
                return cs
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewcs(cs)
                
def previewcs(cs):
    print("No preview available for beat count.")
                
def psizeMenu():
    while True:
        print("Please input the number of chunks in a progression for this Palette (write G or g for random):")
        pt = usrinp()
        if pt in "Gg":
            ps = rselect((2,3,4,5,6))
        else:
            ps = eval(pt)
        while True:
            print(str(ps) + " chunks in a progression. Accept? (Yy, Nn, Pp(preview)):")
            inp = usrinp()
            if inp in "Yy":
                return ps
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewps(ps)
                
def previewps(ps):
    print("No preview available for progression size.")
    
def progcMenu():
    while True:
        print("Please input the number of progressions in a voice for this Palette (write G or g for random):")
        pt = usrinp()
        if pt in "Gg":
            pc = rselect((2,3,4,5,6))
        else:
            pc = eval(pt)
        while True:
            print(str(pc) + " progressions in a voice. Accept? (Yy, Nn, Pp(preview)):")
            inp = usrinp()
            if inp in "Yy":
                return pc
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewpc(pc)
                
def previewpc(pc):
    print("No preview available for voice size.")
    
def scaleInfo(scale):
    print ("Your scale: "+str(scale)[2:-2])
    pianoprinter.octoPrint(scale._notes)
    print("Chords |Short  |Normal |Large  ")
    print("Minor  |" + str(len(scale.getChords("minor", "short"))) + "      |" + str(len(scale.getChords("minor", "normal"))) + "      |" + str(len(scale.getChords("minor", "large"))) + "      ")
    print("Weird  |" + str(len(scale.getChords("weird", "short"))) + "      |" + str(len(scale.getChords("weird", "normal"))) + "      |" + str(len(scale.getChords("weird", "large"))) + "      ")
    print("Major  |" + str(len(scale.getChords("major", "short"))) + "      |" + str(len(scale.getChords("major", "normal"))) + "      |" + str(len(scale.getChords("major", "large"))) + "      ")
    
def scaleMenu():
    while True:
        print("Please input the list of 7 notes in the Scale (ex: 'C Ds E ...'), a smaller list to autocomplete, or write G or g for random:")
        scalet = usrinp()
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
            scaleInfo(scale)
            print()
            print ("Accept? (Yy, Nn, Pp(preview)):")
            inp = usrinp()
            if inp in "Yy":
                return scale
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewscale(scale)
                
def previewscale(scale):
    sidePlay(scale.sample())
            
def paletteMenu():
    while True:
        print("Starting Palette creation:")
        bpm = bpmMenu()
        csize = csizeMenu()
        progsize = psizeMenu()
        progcount = progcMenu()
        scale = scaleMenu()
        pal = musictheory.palette(scale, progsize, progcount, csize)
        pal._bpm = bpm
        while True:
            print("Palette created, Accept? Yy Nn(redo) Qq(quit):")
            inp = usrinp()
            if inp in "Yy":
                name = nameMenu()
                paletteEdit(pal, name)
                return
            elif inp in "Nn":
                print("Retrying:")
                break
            elif inp in "Qq":
                return
        
def nameMenu():
    while True:
        print("Name this palette (will be used as filename):")
        name = usrinp()
        if name in existingPalNames():
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("WARNING: this name already existis in saved palettes, using it and saving will delete the old palette")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        while True:
            print(name + ", is this name ok? Yy Nn:")
            inp = usrinp()
            if inp in "Yy":
                return name
            elif inp in "Nn":
                break
            
def paletteEdit(pal, name): # Main palette edition thing, can enter theme or prog edition
    print("Entering palette edition interface for palette: "+name)
    if pal._n1 == None:
        cprogN1 = None
    else:
        cprogN1 = pal._n1._cprog
    if pal._n2 == None:
        cprogN2 = None
    else:
        cprogN2 = pal._n2._cprog
    if pal._ch == None:
        cprogCH = None
    else:
        cprogCH = pal._ch._cprog
    if pal._bg != None:
        cprogCH = pal._bg._cprog
    try:
        while True:
            print("Editing palette: "+name)
            try:
                bpm = pal._bpm
            except:
                print("Warning: this palette is from an old version of the mikezart environement and does not have an assotitated bpm value!")
                print("Please define bpm in the palette edit menu")            
            if cprogN1 == None:
                print ("Warning: undefined chord progression: Verses 1!")
            if cprogN2 == None:
                print ("Warning: undefined chord progression: Verses 2!")
            if cprogCH == None:
                print ("Warning: undefined chord progression: Chorus/Bridge!")
            if pal._n1 == None:
                print ("Warning: undefined Theme: Verses 1!")
            if pal._n2 == None:
                print ("Warning: undefined Theme: Verses 2!")
            if pal._ch == None:
                print ("Warning: undefined Theme: Chorus!")
            if pal._bg == None:
                print ("Warning: undefined Theme: Bridge!")
            if pal._ge == None:
                print ("Warning: undefined Theme: General!")
            print("Cc - Define chord Progressions")
            print("Tt - Create a Theme")
            print("Ee - Edit a Theme")
            print("Dd - Display Palette Properties")
            print("Ii - Scale Info")
            print("Ss - Save Palette")
            print("Nn - Change Name/filename")
            print("Bb - Change Song BPM")
            print("Qq - Quit")
            inp = usrinp()                       
            if inp in "Cc":
                res = cprogMenu(pal, cprogN1, cprogN2, cprogCH)
                if res == False:
                    res = False
                elif res[0] == "n1":
                    cprogN1 = res[1]
                elif res[0] == "n2":
                    cprogN2 = res[1]
                elif res[0] == "ch":
                    cprogCH = res[1] 
            elif inp in "Tt":
                createThemeMenu(pal, cprogN1, cprogN2, cprogCH)
            elif inp in "Ee":
                chooseThemeEditMenu(pal)
            elif inp in "Dd":
                dispPropMenu(pal, name) 
            elif inp in "Ii": 
                scaleInfo(pal._scale)
            elif inp in "Ss":
                savePalette(pal, name)
            elif inp in "Nn":
                print("Old name: "+name)
                name = nameMenu()
            elif inp in "Bb":
                try:
                    print("Old BPM:", pal._bpm)
                except:
                    print("This palette did not have an assiciated bpm value")
                pal._bpm = bpmMenu()
            elif inp in "Qq":
                print("Warning: Unsaved Changes will be LOST: use Qq to quit or anything else to return to menu")
                inp = usrinp()
                if inp == "q" or inp == "Q" or inp == "Qq" or inp == "qQ":
                    print("Exiting palette edition interface")
                    return
                print("Returning to menu")
    except Exception as e:
        skull()
        print("Something went very wrong during this session of mikezario!")
        print("Please inform the developers of what happened.")
        print("This was the thrown exception that caused the program to crash:")
        print(e)
        print("You have on last chance to save your work before exiting.")
        savePalette(pal, name)
        exit()
    
def skull():
    print('''                   uuuuuuu\n               uu$$$$$$$$$$$uu\n            uu$$$$$$$$$$$$$$$$$uu\n           u$$$$$$$$$$$$$$$$$$$$$u\n          u$$$$$$$$$$$$$$$$$$$$$$$u\n         u$$$$$$$$$$$$$$$$$$$$$$$$$u\n         u$$$$$$$$$$$$$$$$$$$$$$$$$u\n         u$$$$$$"   "$$$"   "$$$$$$u\n         "$$$$"      u$u       $$$$"\n          $$$u       u$u       u$$$\n          $$$u      u$$$u      u$$$\n           "$$$$uu$$$   $$$uu$$$$"
            "$$$$$$$"   "$$$$$$$"\n              u$$$$$$$u$$$$$$$u\n               u$"$"$"$"$"$"$u\n    uuu        $$u$ $ $ $ $u$$       uuu\n   u$$$$        $$$$$u$u$u$$$       u$$$$\n    $$$$$uu      "$$$$$$$$$"     uu$$$$$$\n  u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$\n  $$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"\n   """      ""$$$$$$$$$$$uu ""$"""\n             uuuu ""$$$$$$$$$$uuu\n    u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$\n    $$$$$$$$$$""""           ""$$$$$$$$$$$"\n     "$$$$$"                      ""$$$$""\n       $$$"                         $$$$"\n''')
    
    
def savePalette(pal, name):
    if name in existingPalNames():
        print("There is already a saveFile with this name, are you sure you want to delete it? Yy-Delete Nn/Qq-Return")
        while True:
            inp = usrinp()
            if inp in "QqNn":
                print("Canceling save Palette")
                return
            elif inp in "Yy":
                print("Existing palette is being deleted, do not close this program now or you will lose both palettes!")
                filezart.deletePalette(name)
                break        
    print("Saving palette to folder: "+"/exports/"+name+"/")
    filezart.makeFolder("../exports/" + name)
    pal.infoToFolder(pal._bpm, "../exports/" + name)
            
def chooseThemeEditMenu(pal):
    if (pal._n1 == None and pal._n2 == None and pal._ch == None and pal._bg == None and pal._ge == None):
        print()
        print("No created Themes to edit!")
        print("Use 't' to create a Theme")
        print("Returning")
        print()
        return
    while True:
        print("Choose Theme to edit:")
        if pal._n1 != None:
            print ("n1 - Verses 1")
        if pal._n2 != None:
            print ("n2 - Verses 2")
        if pal._ch != None:
            print ("ch - Chorus")
        if pal._bg != None:
            print ("bg - Bridge")
        if pal._ge != None:
            print ("ge - General")
        print("Qq - Quit")
        inp = usrinp()
        if inp in "Qq":
            return
        elif inp == "n1":
            if pal._n1 != None:
                themeEdit(pal._n1, pal, "Editing Verses type 1", "n1")
                return
        elif inp == "n2":
            if pal._n2 != None:
                themeEdit(pal._n2, pal, "Editing Verses type 2", "n2")
                return
        elif inp == "ch":
            if pal._ch != None:
                themeEdit(pal._ch, pal, "Editing Chorus", "ch")
                return
        elif inp == "ge":
            if pal._ge != None:
                themeEdit(pal._ge, pal, "Editing General lines", "ge")
                return
        elif inp == "bg":
            if pal._bg != None:
                themeEdit(pal._bg, pal, "Editing Bridge", "bg")
                return
            
def chooseThemeMenu(pal):
    if (pal._n1 == None and pal._n2 == None and pal._ch == None and pal._bg == None and pal._ge == None):
        raise ValueError("No themes to choose from")
    while True:
        print("Choose a Theme:")
        if pal._n1 != None:
            print ("n1 - Verses 1")
        if pal._n2 != None:
            print ("n2 - Verses 2")
        if pal._ch != None:
            print ("ch - Chorus")
        if pal._bg != None:
            print ("bg - Bridge")
        if pal._ge != None:
            print ("ge - General")
        print("Qq - Quit")
        inp = usrinp()
        if inp in "Qq":
            return None
        elif inp == "n1":
            if pal._n1 != None:
                return pal._n1
        elif inp == "n2":
            if pal._n2 != None:
                return pal._n2
        elif inp == "ch":
            if pal._ch != None:
                return pal._ch
        elif inp == "ge":
            if pal._ge != None:
                return pal._ge
        elif inp == "bg":
            if pal._bg != None:
                return pal._bg
            
def dispPropMenu(pal, name):
    print()
    print("Displaying Properties of Palette: "+name)
    try:
        print("BPM:", pal._bpm)
    except:
        print("Warning: this palette is from an old version of the mikezart environement and does not have an assotitated bpm value!")
        print("Please define bpm in the palette edit menu")
    print("Csize:", pal._csize)
    print("Progsize:", pal._progsize)
    print("Progcount:", pal._progcount)
    print("Scale:", pal._scale)
    print ("Created Themes:")
    if pal._n1 != None:
        print ("    Verses 1")
    if pal._n2 != None:
        print ("    Verses 2")
    if pal._ch != None:
        print ("    Chorus")
    if pal._bg != None:
        print ("    Bridge")
    if pal._ge != None:
        print ("    General")
    print()
    return
            
def createThemeMenu(pal, cprogN1, cprogN2, cprogCH):
    if (cprogN1 == None and cprogN2==None and cprogCH==None):
        print()
        print("No chord progression defined, cannot create Themes!")
        print("Please define CProgs with 'c'")
        print("Returning to main Palette Menu")
        print()
        return
    while True:
        print("Creating Themes")
        if(pal._n1 != None or pal._n2 != None or pal._ch != None or pal._ge != None or pal._bg != None):
            print ("Created Themes:")
            if pal._n1 != None:
                print ("Verses 1")
            if pal._n2 != None:
                print ("Verses 2")
            if pal._ch != None:
                print ("Chorus")
            if pal._bg != None:
                print ("Bridge")
            if pal._ge != None:
                print ("General")
        print("WARNING: Creating existing Themes will delete old ones")
        if cprogN1 != None:
            print("n1 - Create Verses 1 Theme")
            print("ge - Create General Theme (will have n1 cprog but should not have chordic mmovs)")
        if cprogN2 != None:
            print("n2 - Create Verses 2 Theme")
        if cprogCH != None:
            print("bg - Create Bridge Theme")
            print("ch - Create Chorus Theme")
        print("Qq - Quit")
        inp = usrinp()
        if inp in "Qq":
            return
        elif inp == "n1":
            if cprogN1 != None:
                print("Creating Verses 1 Theme")
                if pal._n1 != None:
                    print("This theme already exists, are you sure you want to override? Yy Nn")
                    while True:
                        inp = usrinp()
                        if inp in "Yy":
                            print("Overriding")
                            pal._n1 = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
                            break
                        elif inp in "Nn":
                            print("Canceling")
                            break
                else:
                    pal._n1 = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
        elif inp == "ge":
            if cprogN1 != None:
                print("Creating General Theme")
                if pal._ge != None:
                    print("This theme already exists, are you sure you want to override? Yy Nn")
                    while True:
                        inp = usrinp()
                        if inp in "Yy":
                            print("Overriding")
                            pal._ge = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
                            break
                        elif inp in "Nn":
                            print("Canceling")
                            break
                else:
                    pal._ge = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
        elif inp == "n2":
            if cprogN2 != None:
                print("Creating Verses 2 Theme")
                if pal._n2 != None:
                    print("This theme already exists, are you sure you want to override? Yy Nn")
                    while True:
                        inp = usrinp()
                        if inp in "Yy":
                            print("Overriding")
                            pal._n2 = musictheory.theme(pal._scale, cprogN2, pal._progcount, pal._csize)
                            break
                        elif inp in "Nn":
                            print("Canceling")
                            break
                else:
                    pal._n2 = musictheory.theme(pal._scale, cprogN2, pal._progcount, pal._csize)
        elif inp == "bg":
            if cprogCH != None:
                print("Creating Bridge Theme")
                if pal._bg != None:
                    print("This theme already exists, are you sure you want to override? Yy Nn")
                    while True:
                        inp = usrinp()
                        if inp in "Yy":
                            print("Overriding")
                            pal._bg = musictheory.theme(pal._scale, cprogCH, pal._progcount, pal._csize)
                            break
                        elif inp in "Nn":
                            print("Canceling")
                            break
                else:
                    pal._bg = musictheory.theme(pal._scale, cprogCH, pal._progcount, pal._csize)
        elif inp == "ch":
            if cprogCH != None:
                print("Creating Chorus Theme")
                if pal._ch != None:
                    print("This theme already exists, are you sure you want to override? Yy Nn")
                    while True:
                        inp = usrinp()
                        if inp in "Yy":
                            print("Overriding")
                            pal._ch = musictheory.theme(pal._scale, cprogCH, pal._progcount, pal._csize)
                            break
                        elif inp in "Nn":
                            print("Canceling")
                            break
                else:
                    pal._ch = musictheory.theme(pal._scale, cprogCH, pal._progcount, pal._csize)
    
def cprogMenu(pal, cprogN1, cprogN2, cprogCH): # Edit progressions for palette, returns (id, prog) or False if failed
    while True:
        print("Note: changed progressions are only taken into effect if their themes are recreated")
        if cprogN1 == None:
            print ("n1 - Define Verses 1 chord Progression     (undefined!)")
        else:
            print ("n1 - Define Verses 1 chord Progression")
        if cprogN2 == None:
            print ("n2 - Define Verses 2 chord Progresion      (undefined!)")
        else:
            print ("n2 - Define Verses 2 chord Progression")
        if cprogCH == None:
            print ("ch - Define Chorus/Bridge chord Progresion (undefined!)")
        else:
            print ("ch - Define Chorus/Bridge chord Progression")
        print ("Ii - Scale Info")
        print ("Qq - Quit")
        inp = usrinp()
        if inp == "n1":
            prog = makeProgMenu(pal, cprogN1)
            if prog == None:
                prog = False
            else:
                return ("n1", prog)
        elif inp == "n2":
            prog = makeProgMenu(pal, cprogN2)
            if prog == None:
                prog = False
            else:
                return ("n2", prog)   
        elif inp == "ch":
            prog = makeProgMenu(pal, cprogCH)
            if prog == None:
                prog = False
            else:
                return ("ch", prog)
        elif inp in "Ii":
            scaleInfo(pal._scale)
        elif inp in "Qq":
            return False
        
        
def makeProgMenu(pal, prog): # Request progression generation, returns None if failed
    progsize = pal._progsize
    if prog == None:
        prog = [] # list of chord3
        for i in range(progsize):
            prog = prog + ["<UNDEFINED>"]
    while True:
        string = ""
        for chord in prog:
            string = string + str(chord) + " "
        print("Your progression:")
        print(string)
        print("Dd - Define chords")
        print("Vv - Generate Progression with default verses weights")
        print("Cc - Generate Progression with default chorus weights")
        print("Gg - Generate Progression with custom weights")
        print("Ss - Show in piano")
        print("Pp - Preview")
        print("Ii - Scale Info")
        print("Ff - Use Progression as is")
        print("Qq - Quit")
        inp = usrinp()
        if inp in "Dd":
            print("Requesting id in range [0-"+str(progsize-1)+"]")
            cid = idMenu()
            if cid in range(progsize):
                print("Defining chord "+str(cid))
                chord = chordMenu(pal._scale)
                if chord != None:
                    print("Chord defined!")
                    prog[cid] = chord
            else:
                print("Invalid id: " + str(cid))
        elif inp in "Vv":
            prog = list(pal._scale.makeProg(progsize, musictheory.n1ChWeights()[0], musictheory.n1ChWeights()[1]))
        elif inp in "Cc":
            prog = list(pal._scale.makeProg(progsize, musictheory.chChWeights()[0], musictheory.chChWeights()[1])) 
        elif inp in "Gg":
            w0 = customWeightMenu(("short", "normal", "large"))
            if w0 != None:
                w1 = customWeightMenu(("minor", "weird", "major"))
                if w1 != None:
                    prog = list(pal._scale.makeProg(progsize, w0, w1))
        elif inp in "Ss":
            for c in prog:
                if c == "<UNDEFINED>":
                    pianoprinter.octoPrint([])
                else:
                    pianoprinter.octoPrint(c._types)
        elif inp in "Pp":
            previewProg(prog)
        elif inp in "Ii":
            scaleInfo(pal._scale)
        elif inp in "Ff":
            if "<UNDEFINED>" in prog:
                print("Cannot use a progression with undefined chords!")
            else:
                return prog
        elif inp in "Qq":
            return None
        
def previewProg(prog):
    audiolen = (1000*len(prog))+3000
    audio = AudioSegment.silent(audiolen)
    for i in range(len(prog)):
        try:
            audio = audio.overlay(prog[i].sampleAudio(), i*1000)
        except:
            print("Error: non chord in progression!")
    sidePlay(audio)
        
def customWeightMenu(lista): # Create custom weight set for lista, return None if failed
    print("Entering weight set creation for", lista)
    w = {}
    for el in lista:
        while True:
            flag = True
            print("Please input weight of", el)
            print("Qq - Quit")
            inp = usrinp()
            if inp in "Qq":
                return None
            for i in inp:
                if not i in "0123456789":
                    flag = False
            if flag:
                w[el] = eval(inp)
                break
    while True:
        print("Your weight set:", w)
        print("Accept? Yy Nn")
        inp = usrinp()
        if inp in "Yy":
            return w
        elif inp in "Nn":
            return None
                    
def idMenu(): # Request int id, return None if failed
    while True:
        print("Please input id: (Qq-quit)")
        inp = usrinp()
        flag = True
        if inp in "Qq":
            return None
        for i in inp:
            if not i in "0123456789":
                flag = False
        if flag:
            return eval(inp)
        
def chordMenu(scale): # Request chord3 generation, return None if failed
    while True:
        print("Defining chord in scale: "+str(scale))
        print("Input list of 3 notes, separated by spaces")
        print("Input first note in chord")
        print("Rr - Generate")
        print("Tt - Generate With Restraints")
        print("Ii - Scale Info")
        print("Qq - Quit")
        inp = usrinp()
        if inp in "Rr":
            chord = musictheory.chord3.fromScale(scale)
            pianoprinter.octoPrint(chord._types)
            while True:
                print(str(chord)+", accept? Yy Nn")
                inp2 = usrinp()
                if inp2 in "Yy":
                    return chord
                elif inp2 in "Nn":
                    break
        elif inp in "Tt":
            print("Input restraint 1 (leave empty for NONE)")
            res1 = usrinp(True)
            if res1 == "":
                res1 = None
            print("Input restraint 2 (leave empty for NONE)")
            res2 = usrinp(True)
            if res2 == "":
                res2 = None
            chord = rselect(scale.getChords(res1, res2))
            pianoprinter.octoPrint(chord._types)
            while True:
                print(str(chord)+", accept? Yy Nn (Pp-Preview)")
                inp2 = usrinp()
                if inp2 in "Yy":
                    return chord
                elif inp2 in "Nn":
                    break
                elif inp2 in "Pp":
                    previewChord(chord)
        elif inp in "Ii":
            scaleInfo(scale)
        elif inp in "Qq":
            return None
        else:
            notenames = str.split(inp, " ")
            notes = ()
            for i in range(len(notenames)):
                if len(notenames[i]) != 0:
                    notes = notes + (musictheory.mnote.fromName(notenames[i] + "0"),)
            if len(notes) == 1:
                for i in scale.getChords():
                    if i._types[0]._type == notes[0]._type:
                        chord = i
                        break
                pianoprinter.octoPrint(chord._types)
                while True:
                    print(str(chord)+", accept? Yy Nn")
                    inp2 = usrinp()
                    if inp2 in "Yy":
                        return chord
                    elif inp2 in "Nn":
                        break
                
            elif len(notes) == 3:
                chord = musictheory.chord3(notes[0], notes[1], notes[2])
                pianoprinter.octoPrint(chord._types)
                while True:
                    print(str(chord)+", accept? Yy Nn")
                    inp2 = usrinp()
                    if inp2 in "Yy":
                        return chord
                    elif inp2 in "Nn":
                        break

def previewChord(chord):
    sidePlay(chord.sampleAudio())

def themeEdit(theme, pal, introSentence="Editing undefined Theme", tag=None): # Edit an existing theme
    while True:
        print(introSentence)
        print("Chordic Voices:      ", len(theme._voices["chordic"]))
        print("Small Melodic Voices:", len(theme._voices["smelodic"]))
        print("Large Melodic Voices:", len(theme._voices["lmelodic"]))
        print("Percussion Voices:   ", len(theme._voices["percussion"]))
        print("Generic Voices:      ", len(theme._voices["generic"]))
        print("Vv - Create a Voice")
        print("Ee - Edit a Voice")
        print("Ss - Edit Voice Sorting") #UNDEFINED
        print("Aa - Preview Audio")
        print("Dd - Display Theme Properties") #UNDEFINED 
        print("Ii - Scale Info") #UNDEFINED
        print("Qq - Quit")
        inp =  usrinp()
        if inp in "Vv":
            print("Choose the type of the voice you are going to create:")
            typ = requestTypeMenu() 
            if typ == None:
                print("Returning")
            else:
                inst = chooseInstMenu() 
                centre = chooseCentreMenu(musictheory.listNotes(inst))
                mtype = typ
                print("Creating Voice")
                print("...")
                voic = musictheory.voice(inst, centre, theme._scale, mtype)
                voic.autoProg(theme._cprog, theme._progc, theme._csize, 0, None, None)
                print("Your Voice,", voic, ", was created, are you sure you want to add it? Yy Nn")
                while True:
                    inp = usrinp()
                    if inp in "Yy":
                        print("Adding voice")
                        theme.addVoiceAsIs(voic)
                        print("Voice Added")
                        print("Last Voice in its category")
                        print("Last Voice in sorting")
                        break
                    elif inp in "Nn":
                        break
        elif inp in "Ee":
            print("Choose the type and ID of the voice you are going to open")
            typ = requestTypeMenu()
            if typ == None:
                print("Returning")
            elif len(theme._voices[typ]) == 0:
                print("You have not created Voices Here!")
            else:
                print("You have", len(theme._voices[typ]), "created voices")
                counter = 0
                for voic in theme._voices[typ]:
                    print(counter, "->", voic)
                    counter = counter+1
                print("Please input an ID in range [0-"+str(len(theme._voices[typ])-1)+"]")
                vid = idMenu()
                if vid >= len(theme._voices[typ]):
                    print("ID out of range")
                else:
                    editVoiceMenu(theme._voices[typ][vid], theme, pal)
        elif inp in "Aa":
            previewThemeAudioMenu(theme, pal, tag)
        elif inp in "Qq":
            return
        
def previewThemeAudioMenu(theme, pal, tag): 
    try:
        print("Please specify parameters:")
        print("Input intensity [0-1]")
        intensity=eval(usrinp())
        print("Input size [0-1]")
        size=eval(usrinp())
        print("Input general lines overlay [0-1]")
        gen=eval(usrinp())
        print("Input chorus lines overlay [0-1]")
        cho=eval(usrinp())
        part = markovzart2.Part(tag, intensity, size, gen, cho)
        sidePlay(part.getAudio(pal, pal._bpm))
    except Exception as e:
        print("Something went very wrong")
        print("Your exception:", e)
        print("...\nReturning\n...")

def requestTypeMenu(): # Request mtype for voice creation or selection, returns None if canceled
    print("Requesting Voice Type")
    print("(Note that there can be percussion voices listed as smelodic or lmelodic)")
    print("Cc - Chordic    (lines repeat once for every chunk but adjusted to chord)")
    print("Ss - SMelodic   (lines repeat once for every progression)")
    print("Ll - LMelodic   (lines repeat once for every voice)")
    print("Pp - Percussion (lines repeat every chunk)")
    print("Gg - Generic    (lines repeat every chunk)")
    print("Qq - Quit")
    while True:
        inp = usrinp()
        if inp in "Cc":
            print("Selected type: Chordic")
            return "chordic"
        if inp in "Ss":
            print("Selected type: SMelodic")
            return "smelodic"
        if inp in "Ll":
            print("Selected type: LMelodic")
            return "lmelodic"
        if inp in "Pp":
            print("Selected type: Percussion")
            return "percussion"
        if inp in "Gg":
            print("Selected type: Generic")
            return "generic"
        if inp in "Qq":
            return None
    
def chooseInstMenu():
    while True:
        print("Please choose the instrument you want to use:")
        print("Write the name of the instrument to select it")
        print("Write the name of a pack to list all instruments in it")
        print("Ii - Show All Instruments")
        print("Pp - Show All Packs")
        inp = usrinp()
        if inp in "Ii":
            printInsts(filezart.getInfo())
        elif inp in "Pp":
            printPacks()
        else:
            try:
                inst = filezart.getInstrument(inp)
                print("Found instrument:", inst, ", use this? Yy, Nn")
                while True:
                    inp = usrinp()
                    if inp in "Yy":
                        return inst
                    elif inp in "Nn":
                        break
            except:
                try:
                    print(inp)
                    pack = filezart.getPack(inp)
                    printInsts(pack)
                except:
                    print("No pack or instrument found:", inp)
                    
def printInsts(insts):
    print("Selected instruments:")
    for inst in insts:
        notes = musictheory.listNotes(inst)
        bot = min(notes)
        top = max(notes)
        print(inst._name)
        print(inst._type)
        print(bot, "-", top)
        print()
    return

def printPacks():
    for i in filezart.getPacks():
        print(i + " "+" "*(14-len(i))+str(len(filezart.getPack(i))))
        
def chooseCentreMenu(notes):
    bot = min(notes)
    top = max(notes)
    while True:
        print("Please choose the central note of your Voice")
        print("If this is a percussion instrument you can choose any note")
        print("Highest Note:", top)
        print("Lowest Note:", bot)
        print("Write the note you want")
        print("Ss - Show All Notes")
        print("Mm - Select Middle Note")
        print("Rr - Select Random Note")
        inp = usrinp()
        if inp in "Ss":
            for note in notes:
                print(note)
            selected = None
        elif inp in "Mm":
            selected = notes[len(notes)//2]            
        elif inp in "Rr":
            selected = rselect(notes)
        else:
            try:
                selected = mnote.fromName(inp)
            except:
                selected = None
                print("Invalid note: "+inp)
        if selected != None:
            while True:
                print("Your Note:",selected)
                print("Use this? Yy Nn")
                inp = usrinp()
                if inp in "Yy":
                    return selected
                if inp in "Nn":
                    break

def editVoiceMenu(voice, theme, pal):
    undoer = copy.deepcopy(voice)
    while True:
        print("Editing",voice)
        print("Rr - Full Auto-Generation") 
        print("Gg - Custom Auto-Generation") 
        print("Mm - Mimic")
        print("Ee - Add/Edit Notes/MMovs") #UNDEFINED 
        print("Aa - Apply Notes to MMovs") #UNDEFINED 
        print("Ii - Show Info") #UNDEFINED
        print("Vv - Change Volume") #UNDEFINED
        print("Pp - Change Pan") #UNDEFINED
        print("Tt - Tab")
        print("Pp - Preview Voice") #UNDEFINED 
        print("Cc - Preview in Context") #UNDEFINED 
        print("Uu - Undo (only last state saved)")
        print("Dd - Delete this Voice") #UNDEFINED
        print("Qq - Quit")
        inp = usrinp()
        
        if inp in "Rr":
            print("Copying to undo clipboard...")
            undoer = copy.deepcopy(voice)
            autoGen(voice, theme, pal)
            print(voice.toTab()+"\n")
            
        elif inp in "Gg":
            print("Copying to undo clipboard...")
            undoer = copy.deepcopy(voice)
            customGen(voice, theme, pal)
            print(voice.toTab()+"\n")
            
        elif inp in "Mm":
            print("Copying to undo clipboard...")
            undoer = copy.deepcopy(voice)
            mimicMenu(voice, theme, pal)
        
        elif inp in "Tt":
            print(voice.toTab()+"\n")
        
        elif inp in "Qq":
            return


def autoGen(voice, theme, pal):
    typ = voice._mtype
    if typ == "chordic":
        ncount = wselect(musictheory.chordicCWeights())
    elif typ == "percussion":
        ncount = wselect(musictheory.percussionCWeights())
    elif typ == "smelodic":
        ncount = wselect(musictheory.smelodicCWeights())
    elif typ == "lmelodic":
        ncount = wselect(musictheory.lmelodicCWeights())
    elif typ == "generic":
        ncount = wselect(musictheory.genericCWeights())
    voice.autoProg(theme._cprog, theme._progc, theme._csize, ncount, None, None)
    print("Voice was auto-generated")

def customGen(voice, theme, pal):
    while True:
        print("Input number of notes per chunk (Qq-quit)")
        inp = usrinp()
        if inp in "Qq":
            return
        try:
            ncount = int(inp)
            break
        except:
            print("Please input a number")
    while True:
        print("Use default weights for this type of voice? Yy Nn (Qq-quit)")
        inp = usrinp()
        if inp in "Yy":
            print("Generating")
            voice.autoProg(theme._cprog, theme._progc, theme._csize, ncount, None, None)
            return
        elif inp in "Nn":
            break
        elif inp in "Qq":
            return
    #User chose custom weights
    while True:
        print("Choosing temporal weights")
        print("C - Use Chordic")
        print("G - Use Generic")
        print("S - Use SMelodic")
        print("L - Use LMelodic")
        print("P - Use Percussion")
        print("W - Create custom Weights")
        inp = usrinp()
        if inp in "Cc":
            tweights = chordicTWeights()
            break
        elif inp in "Gg":
            tweights = genericTWeights()
            break
        elif inp in "Ss":
            tweights = smelodicTWeights()
            break
        elif inp in "Ll":
            tweights = lmelodicTWeights()
            break
        elif inp in "Pp":
            tweights = percussionTWeights()
            break
        elif inp in "Ww":
            print("S - Scale   T - Chord")
            print("R - Repeat  U - Rise    V - Lower")
            tweights = customWeightMenu(("whole","half","quarter"))
            break
    while True:
        print("Choosing movement weights")
        print("C - Use Chordic")
        print("G - Use Generic")
        print("S - Use SMelodic")
        print("L - Use LMelodic")
        print("P - Use Percussion")
        print("W - Create custom Weights")
        inp = usrinp()
        if inp in "Cc":
            mweights = chordicMWeights()
            break
        elif inp in "Gg":
            mweights = genericMWeights()
            break
        elif inp in "Ss":
            mweights = smelodicMWeights()
            break
        elif inp in "Ll":
            mweights = lmelodicMWeights()
            break
        elif inp in "Pp":
            mweights = percussionMWeights()
            break
        elif inp in "Ww":
            mweights = customWeightMenu((mmov("general", "repeat"),mmov("chordic", "repeat"), mmov("chordic", "rise"), mmov("chordic", "lower"), mmov("general", "rise"), mmov("general", "lower")))
            break
    print("Generating")
    voice.autoProg(theme._cprog, theme._progc, theme._csize, ncount, tweights, mweights)
    

    
def mimicMenu(voice, theme, pal):
    print("Entering mimicking menu")
    while True:
        print("Select Voice from local palette? Yy Nn (Qq-quit)")
        inp = usrinp()
        if inp in "Yy":
            break
        elif inp in "Nn":
            print("Please choose a Theme from which to select a voice for mimicking.")
            theme = chooseThemeMenu(pal)
            if theme == None:
                print("Aborting\nReturning")
        elif inp in "Qq":
            print("Returning")
            return
    while True:
        print("Choose the type and ID of the voice you are going to open")
        typ = requestTypeMenu()
        if typ == None:
            print("Returning")
        elif len(theme._voices[typ]) == 0:
            print("You have not created Voices Here!")
        else:
            print("You have", len(theme._voices[typ]), "created voices")
            counter = 0
            for voic in theme._voices[typ]:
                print(counter, "->", voic)
                counter = counter+1
                print("Please input an ID in range [0-"+str(len(theme._voices[typ])-1)+"]")
                vid = idMenu()
                if vid >= len(theme._voices[typ]):
                    print("ID out of range")
                else:
                    print("Mimicking...")
                    voice.mimic(theme._voices[typ][vid])
        
            
    
        
            

mainMenu()
