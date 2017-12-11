import random
from pydub import AudioSegment
from pydub.playback import play
import glob
import operator
import naming
import filezart
import copy
import math
from filezart import instrument
#from multiprocessing import Pool
import threading

def notenames():
    return ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")

def sharpnames():
    return ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


# mnote Musical note class
# type is note independently of octave
class mnote:
    #_value = 0
    #_name = "C0"
    #_typename = "C"
    #_sharpname = "C0"
    #_sharptypename = "C"
    #_type = 0
    #_octave = 0
    
    def __init__(self, value):
        self._value = value
        self._type = value%12
        self._octave = value//12
        self._typename = notenames()[self._type]
        self._sharptypename = sharpnames()[self._type]
        self._name = self._typename + str(self._octave)
        self._sharpname = self._sharptypename + str(self._octave)
        
    def __repr__(self):
        return self._name
    
    def __hash__(self):
        return hash(self._value)
    
    def __eq__(self, other):
        if(isinstance(other, mnote)):
            return (self._value == other._value)
        return False
    
    def __ne__(self, other):
        if(isinstance(other, mnote)):
            return (self._value != other._value)
        return True
    
    def __lt__(self, other):
        return self._value < other._value
    
    @classmethod
    def fromName(cls, name):                                                    # can create as mnote.fromName(noteNameString)
        if "s" in name:
            i = name.index("s")
            name = name[:i] + "#" + name[i+1:]
        if name[0] == "#":
            name = name[1] + name[0] + name[2:]
        elif name[0] == "b":
            if (name[1] != "#") and not (name[1] in "1234567890"):
                name = name[1] + name[0] + name[2:]
        name = uppercase(name[0]) + name[1:]
        if "b" in name:
            typename = name[:2]
            octave = eval(name[2:])
            ntype = notenames().index(typename)
        elif "#" in name:
            sharptypename = name[:2]
            octave = eval(name[2:])
            ntype = sharpnames().index(sharptypename)
        else:
            typename = name[:1]
            octave = eval(name[1:])
            ntype = notenames().index(typename)
        return cls(ntype + octave*12)
    
    def distance(self, other):                                                  # minimum distance of note types
        a = self._type
        b = other._type
        lista = (a-b, b-a, 12+a-b, 12+b-a)
        lista = removeEls(lista, 0, lambda x,y: (x<y))
        return min(lista)
    
    def premier(self, other):                                                   # weird concept, true if self is closer to other from behind, distance should be less than 6
        if (self._type + self.distance(other))%12 == other._type:
            return True
        return False
    
    def isDissonant(self, other):                                               # a.isDissonant(b) returns true if a and b are dissonant notes
        distance = abs(self._type - other._type)
        if distance == 0:
            return False
        elif (distance <= 2) or (distance >= 10):
            return True
        else:
            return False
        
    def isNext(self, other):                                                    # a.isNext(b) returns true if a and b are consecutive notes
        distance = abs(self._type - other._type)
        if distance == 0:
            return False
        elif (distance == 1) or (distance == 11):
            return True
        else:
            return False
        
    def isSame(self, other):                                                    # a.isSame(b) returns true if a an b are the same type notes
        return self._type == other._type
     
    def inChord(self, chord):                                                   # note.inChord(chord) returns true if note exists in chord
        for i in chord._types:
            if self._type == i._type:
                return True
        return False
    
    def inScale(self, scale):                                                   # note.inScale(scale) returns true if note exists in scale
        for i in scale._notes:
            if self._type == i._type:
                return True
        return False
    
    def getAudio(self, inst, bpm):                                              # returns AudioSegment
        return getNote(inst, self)
     
    def approximated(self, other):                                              # returns new note with same type as self but closest to other
        under = mnote((other._octave-1)*12 + self._type)
        same = mnote((other._octave)*12 + self._type)
        over = mnote((other._octave+1)*12 + self._type)
        mdist = min((other.distance(under), other.distance(over), other.distance(same)))
        if other.distance(same) == mdist:
            return same
        if other.distance(over)== mdist:
            return over
        return under
            
     
# MMov beat notation class
# Initialized with movement description
class mmov:
    def __init__(self, ctype, utype):
        self._ctype = ctype                                                     # chordic/general
        self._utype = utype                                                     # rise/lower/repeat
        if ctype == "chordic":
            s = "T"
        elif ctype == "general":
            s = "S"
        else:
            raise ValueError ("Invalid ctype: " + ctype + ".")
        if utype == "rise":
            self._symbol = s + "U"
        elif utype == "lower":
            self._symbol = s + "V"
        elif utype == "repeat":
            self._symbol = s + "R"
        else:
            raise ValueError ("Invalid utype: " + utype + ".")        
            
    def __repr__(self):
        return self._symbol
    
    @classmethod
    def fromName(cls, name):                                                    # can create as mmov.fromName(movNameString)
        if len(name) != 2:
            raise ValueError(name+ " is not a valid MMov name")
        if name[0] in "Tt":
            ctype = "chordic"
        elif name[0] in "Ss":
            ctype = "general"
        else:
            raise ValueError(name+ " is not a valid MMov name")
        if name[1] in "Uu":
            utype = "rise"
        elif name[1] in "Vv":
            utype = "lower"
        elif name[1] in "Rr":
            utype = "repeat"
        else:
            raise ValueError(name+ " is not a valid MMov name")
        return cls(ctype, utype)
    
    def select(self, previous, weights, chord):                                 # returns note to replace this mmov, needs weights of possible notes, last note played, and current chord
        # If there is no previous, select random note from weights or chordic notes
        if(previous == None):
            if(self._ctype == "general"):
                return wselect(weights)
            else:
                d = filterCopyDict(weights, chord, lambda x,y: (not x.inChord(y)))
                try:
                    return wselect(d)
                except:
                    print("Warning, this song might sound bad, a non choridc note had to be chosen as there were none available")
                    return wselect(weights)
            
        if(self._utype == "repeat"):
            return previous
        elif(self._ctype == "general"):
            if(self._utype == "rise"):
                # return weighted selection on copy of weights withot notes lower than previous
                d = filterCopyDict(weights, previous, lambda x,y: (x._value <= y._value))
                if(len(d) == 0):
                    return previous
                return wselect(d)
            else:
                # return weighted selection on copy of weights withot notes higher than previous
                d = filterCopyDict(weights, previous, lambda x,y: (x._value >= y._value))
                if(len(d) == 0):
                    return previous                
                return wselect(d)
        else:
            if(self._utype == "rise"):
                # return weighted selection on copy of weights withot notes lower than previous
                d = filterCopyDict(weights, previous, lambda x,y: (x._value <= y._value))
                d = filterCopyDict(d, chord, lambda x,y: (not x.inChord(y)))
                if(len(d) == 0):
                    return previous
                return wselect(d)
            else:
                # return weighted selection on copy of weights withot notes higher than previous
                d = filterCopyDict(weights, previous, lambda x,y: (x._value >= y._value))
                d = filterCopyDict(d, chord, lambda x,y: (not x.inChord(y)))
                if(len(d) == 0):
                    return previous                
                return wselect(d)            
        
# scale7 Seven note scale class
# can be created with no attributes for random or with list of notes
class scale7:
    def __init__(self, notes=(), octave=False):
        if(octave):
            self._notes = firstOctave()
            return
        self._notes = ()
        if (len(notes)==7):
            for i in notes:
                self._notes = self._notes + (mnote(i._type),)
            self._notes = sorted(self._notes, key=operator.attrgetter('_value'))
        elif (len(notes)==0):
            try:
                self._notes = sorted(self.randnotes(), key=operator.attrgetter('_value'))
            except:
                self._notes = sorted(self.randnotes(), key=operator.attrgetter('_value'))
        elif (len(notes)>7):
            raise ValueError("Generate keys with 7 notes at most")
        else:                                                                   # Can autocomplete smaller list of notes
            self._notes = sorted(self.randcnotes(notes), key=operator.attrgetter('_value'))
            
    @classmethod
    def octave(cls):                                                            # Technically not a scale7, but useful in some cases where one is required
        return cls((), True)
            
    def __repr__(self):
        string = "$-"
        for i in self._notes:
            string = string + i._typename + "-"
        return string + "$"
    
    def randcnotes(self, notes):
        ns = removeElsList(firstOctave(), notes, lambda x,y: (x._value == y._value)) #removeElsList(firstOctave(), notes, lambda x,y: ((x._value == y._value) or (x._value == y._value+1) or (x._value+1 == y._value) or (x._value+11 == y._value) or (x._value == y._value+11)))
        n5 = self.rand5notes(ns)
        c = 0
        while c<100 and n5 == "fail":
            n5 = self.rand5notes(ns)
            c = c+1
        if n5 == "fail":
            print("WARNING: Could not generate a valid Scale from input, generating from random.")
            n5 = self.rand5notes()
        nf= removeElsList(firstOctave(), n5, lambda x,y: (x._value == y._value))
        return nf
            
    def randnotes(self):
        try:
            return removeElsList(firstOctave(), self.rand5notes(), lambda x,y: (x._value == y._value))
        except:
            self.randnotes()
    
    def rand5notes(self, possibilities = False, count=0):
        if (count == 700):
            return "fail"
        if possibilities == False:
            possibilities = firstOctave()
        selecteds = ()
        for i in range(5):
            if len(possibilities) == 0:
                return self.rand5notes(possibilities, count+1)
            note = rselect(possibilities)
            selecteds = selecteds + (note,)
            possibilities = removeEls(possibilities, note, lambda x,y: ((y.isNext(x)) or (y.isSame(x))))
        return selecteds
    
    def getChords(self, arg1=None, arg2=None):                                  # get list of the 7 three note chords in the scale
        chords = ()
        for i in range(len(self._notes)):
            j = (i+2)%7
            k = (j+2)%7
            chords += (chord3(self._notes[i], self._notes[j], self._notes[k]),)
        arg1chords = chords
        if arg1 != None:                                                        # arg1 and arg2 set desired _size and _happ properties of chords
            arg1chords = ()
            for i in chords:
                if (i._size==arg1) or (i._happ==arg1):
                    arg1chords = arg1chords + (i,)
        arg2chords = arg1chords
        if arg2 != None:
            arg2chords = ()
            for i in arg1chords:
                if (i._size==arg2) or (i._happ==arg2):
                    arg2chords = arg2chords + (i,)
        return arg2chords            
    
    def makeProg(self, progsize, arg1dist, arg2dist):                           # Return chord progression of size with selected distributions
        def aux(scale, a1d, a2d):
            arg1 = wselect(a1d)
            arg2 = wselect(a2d)
            chords = scale.getChords(arg1, arg2)
            if len(chords) == 0:
                return aux(scale, a1d, a2d)
            return rselect(chords)
            
        prog = () 
        for i in range(progsize):
            ch = aux(self,arg1dist, arg2dist)
            print(ch)
            if ch in prog:
                print(ch, "retrying")
                ch = aux(self,arg1dist, arg2dist) #if chord is already in prog, it is rerolled to lower odds of repeated chords
                print("retried and got", ch)
            prog = prog + (ch,)
        return prog
    
    def sample(self, inst = filezart.getInstrument("Piano_original")):
        total = (500 * 7) + 3000
        notes = listNotes(inst)
        mednote = notes[len(notes)//2]
        medoct = mednote._octave
        audio = AudioSegment.silent(total)
        t = 0
        for note in self._notes:
            newn = mnote(note._type + (medoct*12))
            noteaudio = newn.getAudio(inst, 60)
            audio = audio.overlay(noteaudio, t)
            t= t+500
        return audio        
        
    
# chord3 Classic 3 note Chord Class
# must be initiated with three notes or fromRandom()
class chord3:
    def __init__(self, note1, note2, note3):
        lista = (mnote(note1._type), mnote(note2._type), mnote(note3._type))
        self._types = self.chordSort(lista)
        self._size = ""                                                         # "short", "normal", "large"
        self._happ = ""                                                         # "minor", "weird", "major"
        self.classify()
    
    def __repr__(self):
        string = "<."
        for i in self._types:
            string = string + i._typename + "."
        return string + ">"
    
    def __eq__(self, other):
        if(isinstance(other, chord3)):
            return (self._types[0]._value == other._types[0]._value)
        return False    
    
    def __hash__(self):
        return self._types[0]._value * self._types[1]._value * self._types[2]._value 
    
    @classmethod
    def fromRandom(cls):                                                        # can create as chord3.fromRandom()
        notes = firstOctave()
        note1 = rselect(notes)
        notes = removeEls(notes, note1, lambda x,y: x.isDissonant(y))
        notes = removeEls(notes, note1, lambda x,y: x.isSame(y))
        note2 = rselect(notes)
        notes = removeEls(notes, note2, lambda x,y: x.isDissonant(y))
        notes = removeEls(notes, note2, lambda x,y: x.isSame(y))
        note3 = rselect(notes)            
        return cls(note1, note2, note3)    
    
    @classmethod
    def fromScale(cls, scale):
        return rselect(scale.getChords())
    
    def chordSort(self, notes):                                                 # puts notes in order of chord
        a = notes[0]
        b = notes[1]
        c = notes[2]
        distAB = a.distance(b)
        distBC = b.distance(c)
        distAC = a.distance(c)
        if (distAB>=distBC) and (distAB>=distAC):
            far1 = a
            far2 = b
            mid = c
        elif (distBC>=distAC) and (distBC>=distAC):
            far1 = b
            far2 = c
            mid = a
        else:
            far1 = a
            far2 = c
            mid = b
        if far1.premier(mid):
            first = far1
            second = mid
            third = far2
        else:
            first = far2
            second = mid
            third = far1
        return (first, second, third)
    
    def classify(self):                                                         # calculates _size and _happ attributes
        a = self._types[0]
        b = self._types[1]
        c = self._types[2]
        leap1 = a.distance(b)
        leap2 = b.distance(c)
        size = leap1 + leap2
        if size > 7:
            self._size = "large"
        elif size < 7:
            self._size = "short"
        else:
            self._size = "normal"
        if leap1 > leap2:
            self._happ = "major"
        elif leap1 < leap2:
            self._happ = "minor"
        else:
            self._happ = "weird"
        return
    
    def sampleAudio(self, inst = filezart.getInstrument("Piano_original")):
        notes = listNotes(inst)
        mednote = notes[len(notes)//2]
        medoct = mednote._octave
        notes = (mnote(self._types[0]._type + 12*medoct),mnote(self._types[1]._type + 12*medoct),mnote(self._types[2]._type + 12*medoct))
        audio = AudioSegment.silent(3000)
        for note in notes:
            noteaudio = note.getAudio(inst, 60)
            audio = audio.overlay(noteaudio,  position=0)
        return audio
  
# Small section of sheet music class
# Initialized with number of beats and chord3(optional)
class chunk:
    def __init__(self, size, chord=None):
        self._size = size
        self._chord = chord
        self._content = [()]*(4*size)                                           # Notes can be placed on half and quarter beats
        
    def __repr__(self):
        st = "|"
        c = 4
        for i in self._content:
            if (c==4):
                c=0
                st = st + "|"
            c = c+1            
            st = st + "."
            for j in i:
                st = st + str(j) + "."
            st = st + "|"
        return st        
    
    def indexof(self, tempo):                                                   # List index corresponding to tempo ex: 0.75 -> 3
        return int(tempo*4)
    
    def set(self, tempo, tupl):
        i = self.indexof(tempo)
        self._content[i] = tupl
        
    def get(self, tempo):
        i = self.indexof(tempo)
        return self._content[i]
    
    def add(self, tempo, note):
        i = self.indexof(tempo)
        self._content[i] = self._content[i] + (note,)
        
    def wholes(self):                                                           # List of whole tempos in chunk
        lista = ()
        for i in range(self._size):
            lista = lista + (i,)
        return lista
            
    def halves(self):                                                           # List of half tempos in chunk
        lista = ()
        for i in range(self._size):
            lista = lista + (i+0.5,)
        return lista
            
    def quarters(self):                                                         # List of quarter tempos in chunk
        lista = ()
        for i in range(self._size):
            lista = lista + (i+0.25, i+0.75)
        return lista
        
    def randMovs(self, count, tweights, mweights):                              # Places count mmov objects with mweights and tweights distribution on chunk              
        for i in range(count):
            mov = wselect(mweights)
            ttype = wselect(tweights)                                           # tweights should be dict of ("whole", "half", "quarter") (note that there are twice as many quarters)
            if ttype == "whole":
                tempo = rselect(self.wholes())
            elif ttype == "half":
                tempo = rselect(self.halves())
            elif ttype == "quarter":
                tempo = rselect(self.quarters())
            else:
                raise ValueError ("Invalid ttype: " + ttype + ".")
            self.add(tempo, mov)
        return
    
    def applyToMovs(self, voic):                                                # Replaces mmovs with mnotes according to voice
        last = None
        for temp in range(len(self._content)):
            newtemp = ()
            lastcandidate = None
            for mov in self._content[temp]:
                if(isinstance(mov, mmov)):
                    sel = mov.select(last,voic._weights, self._chord)
                    newtemp = newtemp + (sel,)
                    lastcandidate = sel
                elif(isinstance(mov, mnote)):
                    newtemp = newtemp + (mov,) #mov is actually a note here
                    lastcandidate = mov
            if lastcandidate != None:
                last = lastcandidate
                self._content[temp] = newtemp
        return
    
    def baseDuration(self, bpm):                                                # Duration of chunk without extra time for last note to play
        beat = bpmToBeat(bpm)
        base = beat*self._size
        return base        
    
    def getAudio(self, inst, bpm):                                              # returns AudioSegment
        beat = bpmToBeat(bpm)
        base = beat*self._size
        total = base + 3000 #extra time for last note to play
        sound = AudioSegment.silent(total)
        
        for temp in range(len(self._content)):
            thissound = AudioSegment.silent(3000)
            for note in self._content[temp]:
                noteaudio = note.getAudio(inst, bpm)
                thissound = thissound.overlay(noteaudio,  position=0)
            sound = sound.overlay(thissound, position=(beat/4)*temp)
        return sound
    
    def clearAudio(self):                                                       # recursive clean of audio cache
        return
        
    def toTab(self):                                                            # return Tab string
        return str(self)
        
# Chord progression class, list of size chunks
# Initialized with size of chunks
class progression:
    def __init__(self, csize):
        self._csize = csize
        self._chunks = ()
        self._audio = None
        self._abpm = 0     
        self._ainst = None
        
    def baseDuration(self, bpm):                                                # Duration of chunk without extra time for last note to play
        beat = bpmToBeat(bpm)
        base = beat*self._csize*len(self._chunks)
        return base     
    
    def getAudio(self, inst, bpm):                                              # check if audio is cached
        if (self._audio == None) or (self._abpm != bpm):
            print("caching")
            return self.forceGetAudio(inst, bpm)
        print("cached")
        return self._audio
    
    def clearAudio(self):                                                       # recursive clean of audio cache
        self._audio = None
        for c in self._chunks:
            c.clearAudio()
    
    def forceGetAudio(self, inst, bpm):                                         # returns AudioSegment
        beat = bpmToBeat(bpm)
        base = beat*self._csize*len(self._chunks)
        total = base + 3000 #extra time for last note to play
        sample = self._chunks[0]
        chunkdur = sample.baseDuration(bpm)
        sound = AudioSegment.silent(total)
        
        for ctime in range(len(self._chunks)):
            caudio = self._chunks[ctime].getAudio(inst, bpm)
            sound = sound.overlay(caudio, position=ctime*chunkdur)
            
        self._audio = sound
        self._abpm = bpm       
            
        return sound    
    
    def toTab(self):                                                             # return Tab string
        stri = ""
        for ch in self._chunks:
            stri = stri + "\n" + ch.toTab()
        return stri
            
        
# Voice Class, identifies instrument, octave zone, stereo and volume information
# Has list of progressions
# Initialized with instrument, centre, mtype(optional), volume(optional), pan(optional)
class voice:
    def __init__(self, instrument, centre, scale, mtype = "chordic", vol = 0, pan = 0): #vol in db added to output, pan in [-1, 1]
        self._inst = instrument
        self._cent = centre
        self._vol = vol
        self._pan = pan
        self._mtype = mtype                                                     # mtype: "generic" "chordic" "smelodic" "lmelodic" "percussion"
        self._scale = scale
        self._weights = {}
        self._progs = ()
        self._audio = None
        self._abpm = 0
        notes = listNotes(instrument)
        notes = removeEls(notes, scale, lambda x,y : ( not(x.inScale(y))))
        for note in notes:
            self._weights[note] = adaptedNormal(centre._value, note._value)
            
    def __repr__(self):
        return "~" + self.getTag() + ":" + self._inst._name + "->" + str(self._cent) + "<-" + str(self._scale)[2:-2] + "~"
    
    def getTag(self):
        try:
            return self._tag
        except:
            return "notag"
        
    def setTag(self, tag):
        self._tag = tag
    
    def become(self, other):                                                                                               # Becomes copy of other voice
        self.__dict__ = copy.deepcopy(other.__dict__)
    
    def autoProg(self, cprog, progcount, csize, ncount=None, tweights=None, mweights=None):                                # Fills voice with progressions
        self._progs = ()
        
        if(self._mtype == "chordic"):
            if tweights == None:
                tweights = chordicTWeights()
            if mweights == None:
                mweights = chordicMWeights()
            if ncount == None:
                ncount = wselect(chordicCWeights())
            rithm = chunk(csize)
            rithm.randMovs(ncount, tweights, mweights) # chordic mtypes repeat rithm but with context sensitive notes for each chord
            prog = progression(csize)
            for chord in cprog:
                nrithm = copy.deepcopy(rithm) #copies selectec rithm
                nrithm._chord = chord         #sets current chord
                nrithm.applyToMovs(self)      #sets notes based on chord
                prog._chunks = prog._chunks + (nrithm,)
            for i in range(progcount):
                self._progs = self._progs + (prog,)
            return
        
        elif(self._mtype == "generic"):
            if tweights == None:
                tweights = genericTWeights()
            if mweights == None:
                mweights = genericMWeights()
            if ncount == None:
                ncount = wselect(genericCWeights())
            rithm = chunk(csize)
            rithm.randMovs(ncount, tweights, mweights) # genetic mtypes repeat chunks
            rithm._chord = cprog[0] #chord of all generic is the first chord in prog but there should be no chordic mmovs and mnotes
            rithm.applyToMovs(self) #sets notes based on scale
            prog = progression(csize)
            for chord in cprog:
                nrithm = copy.deepcopy(rithm)
                prog._chunks = prog._chunks + (nrithm,)
            for i in range(progcount):
                self._progs = self._progs + (prog,)
            return
        
        elif(self._mtype == "smelodic"): # small melodic melodies repeat every progression
            if tweights == None:
                tweights = smelodicTWeights()
            if mweights == None:
                mweights = smelodicMWeights()     
            prog = progression(csize)
            if ncount == None:
                ncount = wselect(smelodicCWeights())
            for chord in cprog:
                rithm = chunk(csize)
                rithm.randMovs(ncount, tweights, mweights)
                rithm._chord = chord
                rithm.applyToMovs(self)
                prog._chunks = prog._chunks + (rithm,)
            for i in range(progcount):
                self._progs = self._progs + (prog,)
            return
        
        elif(self._mtype == "lmelodic"): # large melodic melodies repeat every list of progressions
            if tweights == None:
                tweights = lmelodicTWeights()
            if mweights == None:
                mweights = lmelodicMWeights() 
            if ncount == None:
                ncount = wselect(lmelodicCWeights())    
            for i in range(progcount):
                prog = progression(csize)
                for chord in cprog:
                    rithm = chunk(csize)
                    rithm.randMovs(ncount, tweights, mweights)
                    rithm._chord = chord
                    rithm.applyToMovs(self)
                    prog._chunks = prog._chunks + (rithm,)     
                self._progs = self._progs + (prog,)
            return
        
        elif(self._mtype == "percussion"):
            if tweights == None:
                tweights = percussionTWeights()
            if mweights == None:
                mweights = percussionMWeights()
            if ncount == None:
                ncount = wselect(percussionCWeights())
            rithm = chunk(csize)
            rithm.randMovs(ncount, tweights, mweights) # percussion mtypes repeat chunks, use smelodic or lmelodic for different percussion types
            rithm._chord = cprog[0] #chord of all generic is the first chord in prog but there should be no chordic mmovs and mnotes
            rithm.applyToMovs(self) #sets notes based on scale
            prog = progression(csize)
            for chord in cprog:
                nrithm = copy.deepcopy(rithm)
                prog._chunks = prog._chunks + (nrithm,)
            for i in range(progcount):
                self._progs = self._progs + (prog,)
            return            
        
        else:
            raise ValueError("Invalid mtype: " + self._mtype + ".")
        
    def applyToMovs(self):                                                      # Finds any movs in chunks and replaces them with appropriate notes
        for prog in self._progs:
            for chuc in prog._chunks:
                chuc.applyToMovs(self) 
    
    def mimic(self, other):                                                     # Fills voice with lines mimicking other
        self._progs = ()
        tempCentre = other._cent.approximated(self._cent) # new centre of this voice will be same note as of other but close to original
        delta = tempCentre._value - other._cent._value # how notes of other need to be changed to fit this
        for pro in other._progs:
            newpro = progression(pro._csize)
            for chu in pro._chunks:
                newchu = chunk(chu._size, chu._chord)
                newchu._content = []
                for con in chu._content:
                    beat = ()
                    for note in con:
                        newnote = mnote(note._value+delta) 
                        if newnote in list(self._weights):
                            beat = beat + (newnote,)
                        else:
                            print("Cannot direct mimic trying other octaves")
                            up = mnote(newnote._value+12)
                            down = mnote(newnote._value-12)
                            if up in list(self._weights):
                                print(newnote, "->", up)
                                beat = beat + (up,)
                            elif down in list(self._weights):
                                print(newnote, "->", down)
                                beat = beat + (down,)
                            else:
                                raise ValueError("Cannot force mimic,",newnote,"cannot be forced onto",self._inst)
                    newchu._content = newchu._content+[beat]
                newpro._chunks = newpro._chunks+(newchu,)
            self._progs = self._progs+(newpro,)
    
    def baseDuration(self, bpm):                                                # Duration of chunk without extra time for last note to play
        sample = self._progs[0]
        base = len(self._progs)*sample.baseDuration(bpm)
        return base    
    
    def getAudio(self, bpm):                                                    # check if audio is cached and return it
        if (self._audio == None) or (self._abpm != bpm):
            return self.forceGetAudio(bpm)
        return self._audio
    
    def clearAudio(self):                                                       # recursive delete of audio cache
        self.audio = None
        for p in self._progs:
            p.clearAudio()
        
    def forceGetAudio(self, bpm):                                               # returns AudioSegment, use to override cached audio
        total = 3000 + self.baseDuration(bpm)
        progdur = self._progs[0].baseDuration(bpm)
        sound = AudioSegment.silent(total)
        for progt in range(len(self._progs)):
            print("getting audio of", progt)
            paudio = (self._progs[progt]).getAudio(self._inst, bpm)
            print("overlaying audio of", progt)
            sound = sound.overlay(paudio, progt*progdur)
        print("panning")
        sound = sound.pan(self._pan) + self._vol
        
        self._audio = sound
        self._abpm = bpm
        
        return sound
    
    def toTab(self):                                                            # return Tab string
        stri = ""
        for pr in self._progs:
            stri = stri + "\n" + pr.toTab()
        return stri
    
    def partialAudio(self, size, bpm):                                          # Partial audio to be requested by markovzart2 part
        partialProg = math.ceil(size*len(self._progs)) #number of progressions
        base = self.partialDur(size, bpm)
        progdur = self._progs[0].baseDuration(bpm)
        total = 3000 + base
        sound = AudioSegment.silent(total)
        for progt in range(partialProg):
            paudio = (self._progs[progt]).getAudio(self._inst, bpm)
            sound = sound.overlay(paudio, progt*progdur)
        sound = sound.pan(self._pan) + self._vol
        return sound
        
        
    def partialDur(self, size, bpm):                                           # Partial audio duration to be requested by markovzart2 part
        beat = bpmToBeat(bpm) #duration of a beat
        progdur = self._progs[0].baseDuration(bpm) #duration of a progression
        partialProg = math.ceil(size*len(self._progs)) #number of progressions
        base = partialProg*progdur
        return base         
    
        
# Palette class, list of themes for song
#
class palette:
    def __init__(self, scale, progsize, progcount, csize):
        self._n1 = None #Normal verses 1
        self._n2 = None #Normal verses 2
        self._bg = None #Bridge
        self._ch = None #Chorus
        self._ge = None #General
        
        self._bpm = 110 # DEFAUL BPM MAYBE CHANGE THIS.....
        self._scale = scale
        self._progsize = progsize #chords in progression
        self._progcount = progcount #progressions in voice
        self._csize = csize
        
    def autoProgs(self):                                                        # Create themes with generated progs
        n1prog = self._scale.makeProg(self._progsize, n1ChWeights()[0], n1ChWeights()[1]) #General prog is same as n1 but should have no effect
        n2prog = self._scale.makeProg(self._progsize, n2ChWeights()[0], n2ChWeights()[1])
        chprog = self._scale.makeProg(self._progsize, chChWeights()[0], chChWeights()[1]) #Bridges and choruses have same progressions, for bridges with differente progs use n2
        
        self._n1 = theme(self._scale, n1prog, self._progcount, self._csize) #Normal verses 1
        self._n2 = theme(self._scale, n2prog, self._progcount, self._csize) #Normal verses 2
        self._bg = theme(self._scale, chprog, self._progcount, self._csize) #Bridge
        self._ch = theme(self._scale, chprog, self._progcount, self._csize) #Chorus
        self._ge = theme(self._scale, n1prog, self._progcount, self._csize) #General        
        
    def infoToFolder(self, bpm, folder): # Exports various information and samples to a folder
        filezart.pickleObject(folder + "/pickle.pi", self)
        filezart.makeTextFile(folder + "/scale.txt", str(self._scale))
        
        try:
            filezart.makeFolder(folder + "/n1")
            self._n1.infoToFolder(bpm, folder + "/n1")
        except:
            print("Could not create info of theme n1, palette is saved anyway")
        try:
            filezart.makeFolder(folder + "/n2")
            self._n2.infoToFolder(bpm, folder + "/n2")   
        except:
            print("Could not create info of theme n2, palette is saved anyway")
        try:
            filezart.makeFolder(folder + "/bg")
            self._bg.infoToFolder(bpm, folder + "/bg")     
        except:        
            print("Could not create info of theme bg, palette is saved anyway")
        try:
            filezart.makeFolder(folder + "/ch")
            self._ch.infoToFolder(bpm, folder + "/ch")        
        except:
            print("Could not create info of theme ch, palette is saved anyway")
        try:
            filezart.makeFolder(folder + "/ge")
            self._ge.infoToFolder(bpm, folder + "/ge")            
        except:
            print("Could not create info of theme ge, palette is saved anyway")
        
        
        
# Theme class, list of progressions for palette
# Initialized with scale and chord progression
class theme:
    def __init__(self, scale, cprog, progcount, csize):
        self._scale = scale # scale7
        self._cprog = cprog # chord progression, list of chord3
        self._progc = progcount # number of progressions in Voice
        self._csize = csize #sixe of chunk
        self._voices = {"generic": (), "chordic":(), "smelodic":(), "lmelodic":(), "percussion":()}
        self._sorting = () # List of tvindicator
        
    def addVoice(self, inst, centre, mtype, ncount=None, tweights=None, mweights=None):   # Creates voice and generates progressions for it
        nvoice = voice(inst, centre, self._scale, mtype)                                   ### ncount was here????!             
        nvoice.autoProg(self._cprog, self._progc, self._csize, ncount, tweights, mweights) ### ncount wasnt here?!?
        self._voices[mtype] = self._voices[mtype] + (nvoice,)
        self._sorting = self._sorting + (tvindicator(mtype, len(self._voices[mtype])-1),)
        
    def addVoiceAsIs(self, voic):                                               # Copies voice !!voice should have same parameters as theme!!
        nvoice = copy.deepcopy(voic)
        self._voices[nvoice._mtype] = self._voices[nvoice._mtype] + (nvoice,)
        self._sorting = self._sorting + (tvindicator(voic._mtype, len(self._voices[voic._mtype])-1),)
        
    def previewAudio(self, bpm):                                                # return audio of all voices' first prog
        total = (len(self._cprog)*self._csize*bpmToBeat(bpm)) + 3000
        sound = AudioSegment.silent(total)
        for mtype in list(self._voices):
            for voic in self._voices[mtype]:
                sound = sound.overlay(voic._progs[0].getAudio(voic._inst, bpm))
        return sound                
        
    def infoToFolder(self, bpm, folder): # Exports various information about this theme to a folder
        try:
            filezart.makeTextFile(folder + "/prog.txt", str(self._cprog))
            filezart.makeTextFile(folder + "/sorting.txt", self.sortingString())
            (self.previewAudio(bpm)).export(folder + "/preview.mp3", format = "mp3")
        except:
            print("Could not fully export theme")
        
        for mtype in list(self._voices):
            thisfolder = folder + "/" + mtype
            filezart.makeFolder(thisfolder)
            for i in range(len(self._voices[mtype])):
                try:
                    vfolder = thisfolder+ "/" + str(i)
                    voic = self._voices[mtype][i]
                    filezart.makeFolder(vfolder)
                    filezart.makeTextFile(vfolder + "/tab.txt", voic.toTab())
                    (voic._progs[0].getAudio(voic._inst, bpm)).export(vfolder + "/preview.mp3", format = "mp3")
                except:
                    print("Could not fully export voice")
                
    def sortingString(self):
        string = ""
        for tvi in self._sorting:
            string = string + tvi.indicationStr(self) + "\n"
        return string
    
    def countVoices(self):                                                      # Get number of voices in sorting
        return len(self._sorting)
                
    def baseDurForStruct(self, size, bpm):                                      # Duration to be requested by a markovzart2 Part
        beat = bpmToBeat(bpm) #duration of a beat
        progdur = beat*self._csize*len(self._cprog) #duration of a progression
        partialProg = math.ceil(size*self._progc) #number of progressions
        base = partialProg*progdur
        return base 
        
    def resetSort(self):
        self._sorting = ()
        for mt in list(self._voices):
            for i in range(len(self._voices[mt])):
                self._sorting = self._sorting + (tvindicator(mt, i),)
    
    def shuffleSort(self):
        self.resetSort()
        l = list(self._sorting)
        random.shuffle(l)
        self._sorting = tuple(l)
        
    def findAndDelete(voic):                                                    # locate voice, delete it from voices and from tvindicators
        found = False
        for i in range(len(self._sorting)):
            tvi = self._sorting[i]
            if tvi.getVoice(self) == voic:
                self._sorting = self._sorting[:i] + self._sorting[i+1:]
                found = True
                break
        if not found:
            print("Warning: the voice you are deleting was not found on tvindicators")
        for tip in list(self._voices):
            for i in range(len(self._voices[tip])):
                tvc = self._voices[tip][i]
                if tvc == voic:
                    self._voices[tip] = self._voices[tip][:i] + self._voices[tip][i+1:]
                    return
        print("Warning: the voice you are deleting was not found anywhere!!")
                
        
        
        
# TVIndicator class, pointer for voice in theme
# Initialized with voice mtype and voice id (index on theme mtype list)  
class tvindicator:
    def __init__(self, mtype, index):
        if not mtype in ("generic", "chordic", "smelodic", "lmelodic", "percussion"):
            raise ValueError ("Invalid mtype: "+str(mtype))
        self._mtype = mtype
        self._index = index
        
    def getVoice(self, them):                                                  # get corresponding voice in theme
        return them._voices[self._mtype][self._index]
    
    def indicationStr(self, them):
        return "["+self._mtype+"_"+str(self._index)+str(them._voices[self._mtype][self._index])+"]"
    
    def __repr__(self):
        return "indicator:"+self._mtype+"-"+str(self._index)
        
        
        
        
def uppercase(text):
    ret = ""
    for i in text:
        if i in "abcdefghijklmnopqrstuvwxyz" + chr(231): #chr(231) is lowercase cedilha c
            ret = ret + ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" + chr(199))[("abcdefghijklmnopqrstuvwxyz"+ chr(231)).index(i)]
        else: ret = ret+i
    return ret

def lowercase(text):
    ret = ""
    for i in text:
        if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + chr(199): #chr(199) is uppercase cedilha C
            ret = ret + ("abcdefghijklmnopqrstuvwxyz"+ chr(231))[("ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ chr(199)).index(i)]
        else: ret = ret+i
    return ret    
    
# rselect RandomSelect returns random element of list
def rselect(lista):
    return random.choice(lista)


# wselect WeightedSelect returns element of dictionary based on dict weights {element:weight}
def wselect(dicti):
    if len(list(dicti))==0:
        raise ValueError ("cannot select from empty dict")
    total=0
    for i in list(dicti):
        total = total + dicti[i]
    if total <= 0:
        raise ValueError ("total must be larger than zero")
    indice = total*random.random()
    for i in list(dicti):
        if dicti[i]>=indice:
            return i
        indice = indice - dicti[i]
    raise ValueError ("something went wrong")

# removeEls ElementRemoval returns list without elements that are true for lamb(e, element)
def removeEls(lista, element, lamb):
    size = len(lista)
    for i in range(len(lista)):
        j = size - (i+1)
        if lamb(lista[j], element):
            lista = lista[:j] + lista[j+1:]
    return lista

# filterCopyDict returns copy of dict without elements that are true for lamb(e, element)
def filterCopyDict(dic, element, lamb):
    new = {}
    for i in list(dic):
        if not lamb(i, element):
            new[i] = dic[i]
    return new

# removeElsList ListComparisionElementRemoval returns list without elements that are true for lamb(e, element), where element is every element of list2 
def removeElsList(lista, lista2, lamb):
    size = len(lista)
    for i in range(len(lista)):
        j = size - (i+1)
        for i in lista2:
            if lamb(lista[j], i):
                lista = lista[:j] + lista[j+1:]
                break
    return lista  

#returns string cut after first instance of find. cutafter("43211234", "12") -> "34"
def cutafter(string, find):
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

# firstOctave returns list of notes in first octave, "C0" to "B0"
def firstOctave():
    lista = ()
    for i in range(12):
        lista = lista + (mnote(i),)
    return lista

# Adapted simplified normal distribution probability for note distances (for wselects)
def adaptedNormal(center, value):
    return 10*(2.718281828459045**((-1/20)*((center-value)**2)))

# Beats Per Minute to Beat time, time of each beat with given eats per minute (miliseconds)
def bpmToBeat(bpm):
    return (60 * 1000)/bpm

# Returns sorted copy of list of notes
def noteSort(notes):
    if (len(notes) == 0 or len(notes) == 1):
        return notes
    under = ()
    upper = ()
    anchor = notes[0]
    for i in notes[1:]:
        if i._value < anchor._value:
            under = under + (i,)
        else:
            upper = upper + (i,)
    return noteSort(under) + (anchor,) + noteSort(upper)

# List available notes of instrument
def listNotes(inst):
    if inst._type == "modulation":
        r = inst._rang
        notens = str.split(r, "-")
        first = mnote.fromName(notens[0])
        last = mnote.fromName(notens[1])
        v = first._value
        ns = ()
        while v <= last._value:
            ns = ns + (mnote(v),)
            v = v+1
        return ns
    if (inst._noteslist == ()):
        notes = ()
        notenames = inst.getNoteNames()
        for notename in notenames:
            notes = notes +  (mnote.fromName(notename),)
        notes = noteSort(notes)
        inst._noteslist = notes
    return inst._noteslist

# Get Audiosegment object of instrument note
def getNote(instrument, note):
    if instrument._type == "modulation":
        base = instrument.getAudio(None)
        aud = modulateAudio(base, mnote.fromName(instrument._base), note)
        return aud
    if instrument._type == "percussion":
        return instrument.getAudio(None)
    if instrument._type == "randper":
        return instrument.getAudio(None)    
    if instrument._bmsp == "bemol":
        typen = note._typename
    elif instrument._bmsp == "sharp":
        typen = note._sharptypename
    elif instrument._bmsp == "esse":
        typen = note._sharptypename
        if "#" in typen:
            i = typen.index("#")
            typen = typen[:i] + "s" + typen[i+1:]
    else:
        raise ValueError(instrument._bmsp + " is not a valid sharpType!")   
    
    if instrument._case == "upper":
        typen = uppercase(typen[0]) + typen[1:]
    elif instrument._case == "lower":
        typen = lowercase(typen)
    else:
        raise ValueError(instrument._case + " is not a valid caseType!")
    
    if instrument._nclt == "name_octave":
        final = typen + str(note._octave)
    elif instrument._nclt == "octave_name":
        final = str(note._octave) + typen
    else:
        raise ValueError(instrument._nclt + " is not a valid nomenclatureType!")    
    
    return instrument.getAudio(final)

# Side Play plays audio on parallel process
def sidePlay(audio):
    threading.Thread(target=play, args=(audio,)).start()
    #pool = Pool()
    #pool.apply_async(play, (audio,))  

# Modulate Audio, returns audio of audionote sped up or slowed down to be objetive note
def modulateAudio(audio, audionote, objective):
    
    octaves = (objective._value - audionote._value)/12 
    
    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))

    new = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    
    new = new.set_frame_rate(44100)
 
    return new

def sampleCProg(cprog, inst = filezart.getInfo()[2]):
    audio = AudioSegment.silent((len(cprog)*1000) + 3000)
    t = 0
    for chord in cprog:
        audio = audio.overlay(chord.sampleAudio(inst), t)
        t = t + 1000
    play(audio)
    
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Song Parameters XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#Chordic Parameters
def chordicMWeights():
    return {mmov("general", "repeat"):1,mmov("chordic", "repeat"):4, mmov("chordic", "rise"):4, mmov("chordic", "lower"):4, mmov("general", "rise"):1, mmov("general", "lower"):1}

def chordicTWeights():
    return {"whole":4, "half":2, "quarter":1}

def chordicCWeights():
    return {1:1, 2:2, 3:3, 4:20, 5:20, 6:20, 7:15, 8:14, 9:13, 10:3, 11:2, 12:1}

#Generic Parameters
def genericMWeights():
    return {mmov("general", "repeat"):3,mmov("chordic", "repeat"):1, mmov("chordic", "rise"):1, mmov("chordic", "lower"):1, mmov("general", "rise"):3, mmov("general", "lower"):3}

def genericTWeights():
    return {"whole":4, "half":2, "quarter":1}

def genericCWeights():
    return {1:1, 2:2, 3:3, 4:20, 5:20, 6:20, 7:15, 8:14, 9:13, 10:3, 11:2, 12:1}

#Small Melodic Parameters
def smelodicMWeights():
    return {mmov("general", "repeat"):2,mmov("chordic", "repeat"):4, mmov("chordic", "rise"):4, mmov("chordic", "lower"):4, mmov("general", "rise"):2, mmov("general", "lower"):2}

def smelodicTWeights():
    return {"whole":4, "half":2, "quarter":1}

def smelodicCWeights():
    return {1:1, 2:2, 3:3, 4:20, 5:20, 6:20, 7:15, 8:14, 9:13, 10:3, 11:2, 12:1}

#Percussion Parameters
def percussionMWeights():
    return {mmov("general", "repeat"):1}

def percussionTWeights():
    return {"whole":6, "half":1, "quarter":1}

def percussionCWeights():
    return {1:10, 2:10, 3:10, 4:8, 5:6, 6:5}

#Chord parameters
def n1ChWeights():
    return ({"short":2, "normal":5, "large":2}, {"minor":6, "weird":3, "major":6})

def n2ChWeights():
    return ({"short":2, "normal":5, "large":2}, {"minor":6, "weird":3, "major":6})

def chChWeights():
    return ({"short":2, "normal":5, "large":2}, {"minor":6, "weird":2, "major":10})

    
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Test Area XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def cfill():
    s = scale7()
    inst = filezart.getInfo()[0]
    v = voice(inst, mnote.fromName("F3"),s)    
    cr = chord3.fromScale(s)
    ch = chunk(4, cr)
    ch2 = chunk(4, cr)
    ch3 = chunk(4, cr)
    mw = {mmov("general", "repeat"):2,mmov("chordic", "repeat"):2, mmov("chordic", "rise"):1, mmov("chordic", "lower"):1, mmov("general", "rise"):1, mmov("general", "lower"):1}
    tw = {"whole":4, "half":2, "quarter":1}
    print(ch)
    print(mw)
    print(tw)
    ch.randMovs(8, tw, mw)
    ch2.randMovs(8, tw, mw)
    ch3.randMovs(8, tw, mw)
    print(ch)
    print(ch2)
    print(ch3)
    print(v)
    print(cr)
    ch.applyToMovs(v)
    ch2.applyToMovs(v)
    ch3.applyToMovs(v)
    print(ch)
    print(ch2)
    print(ch3)
    
def vocd():
    inst = filezart.getInfo()[0]
    v = voice(inst, mnote(34), scale7())
    print (inst)
    print (v)
    print (v._weights)
    print (mnote(34), v._weights[mnote(34)])
    print (mnote(33), v._weights[mnote(33)])
    print (mnote(35), v._weights[mnote(35)])
    print (mnote(34+10), v._weights[mnote(34+10)])
    print (mnote(34+20), v._weights[mnote(34+20)])
    
def msel():
    inst = filezart.getInfo()[0]
    v = voice(inst, mnote(34), scale7())
    c = chord3.fromRandom()
    print(v)
    print(c)
    mov1 = mmov("chordic", "rise")
    mov2 = mmov("chordic", "rise")
    mov3 = mmov("chordic", "repeat")
    mov4 = mmov("general", "lower")
    mov4 = mmov("general", "lower")
    note = None
    print (note)
    note = mov1.select(note, v._weights, c)
    print (note)
    note = mov2.select(note, v._weights, c)
    print (note)
    note = mov3.select(note, v._weights, c)
    print (note)
    note = mov4.select(note, v._weights, c)
    print (note)    
    
def auto1plus(n):
    for i in range(n):
        auto1()
        
def auto3plus(n):
    for i in range(n):
        auto3()
    
def auto1():
    s = scale7()
    prog = s.makeProg(4, {"short":2, "normal":5, "large":2}, {"minor":6, "weird":2, "major":8})
    inst = filezart.getInfo()[1]
    instg = filezart.getInfo()[0]
    v1 = voice(instg, mnote(30), s, "chordic")
    v2 = voice(inst, mnote(70), s, "chordic")
    v1.autoProg(prog, 4, 4)
    v2.autoProg(prog, 4, 4)
    
    print(s)
    print(prog)
    print(v1)
    print(v1._progs)
    print(v2)
    print(v2._progs)    
    
    play(v1._progs[0].getAudio(inst, 120))
    play(v2._progs[0].getAudio(inst, 120))
    play((v1._progs[0].getAudio(instg, 120)-20).overlay(v2._progs[0].getAudio(inst, 120)))


def auto2():
    s = scale7()
    prog = s.makeProg(4, {"short":1, "normal":5, "large":1}, {"minor":5, "weird":1, "major":8})
    inst = filezart.getInfo()[1]
    v1 = voice(inst, mnote(30), s, "generic")
    v1.autoProg(prog, 4, 4)
    
    print(s)
    print(prog)
    print(v1)
    print(v1._progs)  
    
    play(v1._progs[0].getAudio(inst, 120))
    
    
def auto3():
    s = scale7()
    prog = s.makeProg(4, {"short":1, "normal":5, "large":1}, {"minor":5, "weird":1, "major":8})
    inst = filezart.getInfo()[1]
    instg = filezart.getInfo()[3]
    v1 = voice(instg, mnote(40), s, "chordic", vol = -20)
    v2 = voice(inst, mnote(40), s, "chordic")
    v1.autoProg(prog, 4, 4)
    v2.autoProg(prog, 4, 4)
    
    print(s)
    print(prog)
    print(v1)
    print(v1._progs)
    print(v2)
    print(v2._progs)    
    
    #play(v1._progs[0].getAudio(instg, 120))
    #play(v2._progs[0].getAudio(inst, 120))
    
    sampleCProg(prog)
    
    play((v1._progs[0].getAudio(instg, 120)).overlay(v2._progs[0].getAudio(inst, 120)-15))

def auto4():
    s = scale7()
    prog = s.makeProg(5, {"short":1, "normal":5, "large":1}, {"minor":5, "weird":1, "major":8})
    inst = filezart.getInfo()[1]
    instg = filezart.getInfo()[3]
    v1 = voice(instg, mnote(40), s, "chordic", vol = -20)
    v2 = voice(inst, mnote(40), s, "chordic")
    v1.autoProg(prog, 5, 5)
    v2.autoProg(prog, 5, 5)
    
    print(s)
    print(prog)
    print(v1)
    print(v1._progs)
    print(v2)
    print(v2._progs)    
    
    #play(v1._progs[0].getAudio(instg, 120))
    #play(v2._progs[0].getAudio(inst, 120))
    
    sampleCProg(prog)
    
    play((v1._progs[0].getAudio(instg, 100)).overlay(v2._progs[0].getAudio(inst, 100)-15))


        
def poop():
    piano = filezart.getInfo()[3]
    for i in listNotes(piano):
        play(getNote(piano, i))
        
def fitest():
    inst = filezart.getInfo()[2]
    a = getNote(inst, mnote(35))
    b = getNote(inst, mnote(60))
    play(a)
    play(b)
    n = AudioSegment.silent(3000)
    n = n.overlay(a)
    n = n.overlay(b)
    play(n)
    
    
def modtest():
    n = AudioSegment.silent(5000)
    t = 0
    for i in ("C3","D3","E3","F3","G3","A3","B3","C4"):
        a = modulateAudio(getNote(filezart.getInfo()[6], mnote.fromName("C3")),mnote.fromName("C3"),mnote.fromName(i))
        n = n.overlay(a,t*500)
        t=t+1
    play(n)
