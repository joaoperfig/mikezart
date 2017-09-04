from musictheory import *
import musictheory
import random
import operator
import pianoprinter
import filezart

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
        print("")
        if acceptEmpty == True:
            return inp
        elif inp != "":
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
    while True:
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
                themeEdit(pal._n1, pal, "Editing Verses type 1")
                return
        elif inp == "n2":
            if pal._n2 != None:
                themeEdit(pal._n2, pal, "Editing Verses type 2")
                return
        elif inp == "ch":
            if pal._ch != None:
                themeEdit(pal._ch, pal, "Editing Chorus")
                return
        elif inp == "ge":
            if pal._ge != None:
                themeEdit(pal._ge, pal, "Editing General lines")
                return
        elif inp == "bg":
            if pal._bg != None:
                themeEdit(pal._ge, pal, "Editing Bridge")
                return
            
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
        print ("Verses 1")
    if pal._n2 != None:
        print ("Verses 2")
    if pal._ch != None:
        print ("Chorus")
    if pal._bg != None:
        print ("Bridge")
    if pal._ge != None:
        print ("General")
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
                pal._n1 = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
        elif inp == "ge":
            if cprogN1 != None:
                print("Creating General Theme")
                pal._ge = musictheory.theme(pal._scale, cprogN1, pal._progcount, pal._csize)
        elif inp == "n2":
            if cprogN2 != None:
                print("Creating Verses 2 Theme")
                pal._n2 = musictheory.theme(pal._scale, cprogN2, pal._progcount, pal._csize)
        elif inp == "bg":
            if cprogCH != None:
                print("Creating Bridge Theme")
                pal._bg = musictheory.theme(pal._scale, cprogCH, pal._progcount, pal._csize)
        elif inp == "ch":
            if cprogCH != None:
                print("Creating Chorus Theme")
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
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                return ("n1", prog)
        elif inp == "n2":
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                return ("n2", prog)   
        elif inp == "ch":
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                return ("ch", prog)
        elif inp in "Ii":
            scaleInfo(pal._scale)
        elif inp in "Qq":
            return False
        
        
def makeProgMenu(pal): # Request progression generation, returns None if failed
    progsize = pal._progsize
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
        
def customWeightMenu(lista): # Create custom weight set for lista, return None if failed
    print("Entering wheight set creation for", lista)
    w = {}
    for el in lista:
        while True:
            flag = True
            print("Please input wheight of", el)
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
        print("Aa - Generate with restraints")
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
        elif inp in "Aa":
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
                print(str(chord)+", accept? Yy Nn")
                inp2 = usrinp()
                if inp2 in "Yy":
                    return chord
                elif inp2 in "Nn":
                    break
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


def themeEdit(theme, pal, introSentence="Editing undefined Theme"): # Edit an existing theme
    while True:
        print(introSentence)
        print("Chordic Voices:", len(theme._voices["chordic"]))
        print("Small Melodic Voices:", len(theme._voices["smelodic"]))
        print("Large Melodic Voices:", len(theme._voices["lmelodic"]))
        print("Percussion Voices:", len(theme._voices["percussion"]))
        print("Generic Voices:", len(theme._voices["generic"]))
        print("Vv - Create a Voice")
        print("Ee - Edit a Voice")
        print("Aa - Preview Audio") #UNDEFINED 
        print("Dd - Display Theme Properties") #UNDEFINED 
        print("Ii - Scale Info") #UNDEFINED
        inp =  usrinp()
        if inp in "Vv":
            print("Choose the type of the voice you are going to create:")
            typ = requestTypeMenu() 
            if typ == None:
                print("Returning")
            else:
                inst = chooseInstMenu() 
                centre = chooseCentreMenu(musictheory.listNotes(inst)) ####
                mtype = typ
                print("Creating Voice")
                print("...")
                voic = musictheory.voice(inst, centre, them._scale, mtype)
                print("Your Voice", voic, "was created, are you sure you want to add it?")
        elif inp in "Ee":
            print("Choose the type and ID of the voice you are going to open")
            typ = requestTypeMenu()
            if typ == None:
                print("Returning")
            elif len(them._voices[typ]) == 0:
                print("You have not created Voices Here!")
            else:
                print("Please input an ID in range [0-"+str(len(them._voices[typ])-1)+"]")
                vid = idMenu()
                if vid >= len(them._voices[typ]):
                    print("ID out of range")
                else:
                    editVoiceMenu(them._voices[typ][vid]) #####

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
            return "chordic"
        if inp in "Ss":
            return "smelodic"
        if inp in "Ll":
            return "lmelodic"
        if inp in "Pp":
            return "percussion"
        if inp in "Gg":
            return "generic"
        if inp in "Qq":
            return None
    
def chooseInstMenu():
    while True:
        print("Please choose the instrument you want to use:")
        print("Write the name of the instrument to select it")
        print("Write the name of a pack to list all instruments in it")
        print("Ii - Show all isntruments")
        print("Pp - Show all packs")
        inp = usrinp()
        if inp in "Ii":
            printInsts(filezart.getInfo())
        if inp in "Pp":
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
                    pack = filezart.getPack(inp)
                    printInsts(insts)
                except:
                    print("No pack or instrument found:", inp)
                    
def printInsts(insts):
    return
    
        


mainMenu()
