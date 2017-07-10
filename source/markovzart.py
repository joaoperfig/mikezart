import filezart
import random

class Part:
    
    def __init__(self, typ=None, intensity=0, size=0, gen=0, cho=0):
        self._type = typ #"n1", "n2", "bg", "ch", "ge"
        if intensity<0 or gen<0 or cho<0 or size<0 or intensity>1 or size>1 or gen>1 or cho>1:
            raise ValueError ("Invalid Values for Structure Part")
        self._intensity = intensity # [0-1]
        self._size = size # [0-1]
        self._genover = gen # [0-1] overlay of general type lines
        self._chover = cho # [0-1] overlay of chord type lines
        
    def __repr__(self):
        return "[" + self._type + "-" + str(self._intensity) + "-" + str(self._size) + "-" + str(self._genover) + "-" + str(self._chover) + "]"
        
    @classmethod
    def fromString(cls, string): # [n1-0.123-0.321]
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


class Structure:
    
    def __init__(self):
        self._parts = ()
        
    def add(self, part):
        self._parts = self._parts+(part,)
    
    def __repr__(self):
        return "@STRUCTURE:" + str(self._parts)
 
 
class Markov:
    
    def __init__(self):
        self._dict = {"n1":(), "n2":(), "bg":(), "ch":(), "ge":()}
        self._start = ()
        self._end = ()
        self._size = {}
        
    def addData(self, song): #song should be string of parts separated by commas, !NO COMMA AT THE END!
        if len(song)<8:
            return
        partstrings = str.split(song, ",")
        parts = ()
        for partstring in partstrings:
            parts = parts + (Part.fromString(partstring),) #turn part strings into part objects and put them in list\
        self._size = dicinc(self._size, len(parts))  #add song size to sizes distribution
        for i in range(len(parts)):
            if i==0:
                last = parts[0]
                self._start = self._start+(parts[0],) #add to start list
            else:
                self._dict[last._type] = self._dict[last._type] + (parts[i],) #add to list of previous type
                last = parts[i]
            if i==len(parts)-1:
                self._end = self._end + (parts[i],) #add to end list
                
    def makeStruct(self): #generates a structure from data
        size = wselect(self._size)
        struct = Structure()
        for i in range(size):
            if i==0:
                part = rselect(self._start)
                last = part
                struct.add(part)
            if i==size-1:
                part = rselect(self._end)
                last = part
                struct.add(part)
            else:
                part = rselect(self._dict[last._type])
                last = part
                struct.add(part)
        return struct
                
                
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



def readData(filename): #"../resources/*.txt"
    markovs = filezart.getMarkov()
    data = filezart.readLines(filename)
    for song in data:
        markovs.addData(song)
    filezart.saveMarkov(markovs)
    
def learnData(string):
    if len(string)<8:
        return
    markovs = filezart.getMarkov()
    markovs.addData(string)
    filezart.saveMarkov(markovs)
        

def dicinc(dic, el):
    if el in list(dic):
        dic[el] = dic[el] + 1
    else:
        dic[el] = 1
    return dic

def learnMode():
    print("Welcome to markovzart input learnMode")
    while True:
        print("Write M to start a song, Q to quit")
        inp = raw_input(">")
        if inp=="M" or inp=="m":
            song = ""
            while True:
                print("Write the type (n1, n2, ge, bg, ch), followed by space, intensity and optional (size=1, gen=0, cho=0), or S to stop")
                print("Song: "+str(song))
                inp = raw_input(">")
                if inp == "S" or inp == "s":
                    print ("Save song to main memory? Y N C (yes, no, cancel)")
                    inp = raw_input (">")
                    if inp == "y" or inp == "Y":
                        print("Saving")
                        learnData(song)
                        song = ""
                        break
                    elif inp == "N" or inp=="n":
                        print("Deleting song")
                        song = ""
                        break
                    elif inp == "C" or inp=="c":
                        print("Returning")
                    else:
                        print("Unknown input, Returning")
                elif inp[:2] in ("n1", "n2", "ge", "bg", "ch"):
                    part = tuple(str.split(inp, " "))
                    if len(part)<2:
                        part = part + ("0.5",)
                    if len(part)<3:
                        part = part + ("1",)
                    if len(part)<4:
                        part = part + ("0",)
                    if len(part)<5:
                        part = part + ("0",)
                    if len(song)!= 0:
                        song = song + ", "
                    song = song + "[" + part[0] + "-" + part[1] + "-" + part[2] + "-" + part[3] + "-" + part[4] + "]"
                else:
                    print("Unknown input")
        elif inp=="q" or inp=="Q":
            return
        else:
            print("Unknown input")
            
learnMode()
            
