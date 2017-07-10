import filezart
import random

class Part:
    
    def __init__(self, typ=None, intensity=0, size=0):
        self._type = typ #"n1", "n2", "bg", "ch", "ge"
        if intensity<0 or size<0 or intensity>1 or size>1:
            raise ValueError ("Invalid Values for Structure Part")
        self._intensity = intensity # [0-1]
        self._size = size # [0-1]
        
    def __repr__(self):
        return "[" + self._type + "-" + str(self._intensity) + "-" + str(self._size) + "]"
        
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
        return cls(typ, inten, size)


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
        

def dicinc(dic, el):
    if el in list(dic):
        dic[el] = dic[el] + 1
    else:
        dic[el] = 1
    return dic

print(filezart.getMarkov().makeStruct())
