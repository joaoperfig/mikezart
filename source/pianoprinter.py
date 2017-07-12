import musictheory
import operator


#    l1 = " _______________________________________  "
#    l2 = "|  | | | |  |  | | | | | |  |  | | | |  | "
#    l3 = "|  | | | |  |  | | | | | |  |  | | | |  | "
#    l4 = "|  | | | |  |  | | | | | |  |  | | | |  | "
#    l5 = "|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  | "
#    l6 = "|   |   |   |   |   |   |   |   |   |   | "
#    l7 = "|   |   |   |   |   |   |   |   |   |   | "
#    l8 = "|___|___|___|___|___|___|___|___|___|___| "


class pnote:
    
    def __init__(self, value, on):
        self._value = value
        self._type = value%12
        self._on = on
        
    def strings(self):
        on = self._on
        if self._type in (0, 5):
            if on:
                l1 = "___"
                l2 = "██|"
                l3 = "██|"
                l4 = "██|"
                l5 = "██|_"
                l6 = "███|"
                l7 = "███|"
                l8 = "███|"
            else:
                l1 = "___"
                l2 = "  |"
                l3 = "  |"
                l4 = "  |"
                l5 = "  |_"
                l6 = "   |"
                l7 = "   |"
                l8 = "___|"
        elif self._type in (1, 3, 6, 8, 10):
            if on:
                l1 = "__"
                l2 = "█|"
                l3 = "█|"
                l4 = "█|"
                l5 =  "|"
                l6 =  ""
                l7 =  ""
                l8 =  ""
            else:
                l1 = "__"
                l2 = " |"
                l3 = " |"
                l4 = " |"
                l5 =  "|"
                l6 =  ""
                l7 =  ""
                l8 =  ""
        elif self._type in (2, 7, 9):
            if on:
                l1 =  "__"
                l2 =  "█|"
                l3 =  "█|"
                l4 =  "█|"
                l5 =  "█|_"
                l6 = "███|"
                l7 = "███|"
                l8 = "███|"
            else:
                l1 =  "__"
                l2 =  " |"
                l3 =  " |"
                l4 =  " |"
                l5 =  " |_"
                l6 = "   |"
                l7 = "   |"
                l8 = "___|"
        elif self._type in (4, 11):
            if on:
                l1 =  "___"
                l2 =  "██|"
                l3 =  "██|"
                l4 =  "██|"
                l5 =  "██|"
                l6 = "███|"
                l7 = "███|"
                l8 = "███|"
            else:
                l1 =  "___"
                l2 =  "  |"
                l3 =  "  |"
                l4 =  "  |"
                l5 =  "  |"
                l6 = "   |"
                l7 = "   |"
                l8 = "___|"
        else:
            print(self._type)
            raise ValueError ("poopiano")
        return (l1, l2, l3, l4, l5, l6, l7, l8)
            
def pstring(pnotes):
    ls = [" _", " |", " |", " |", " |", " |", " |", " |"]
    for n in pnotes:
        s = n.strings()
        for i in range(len(s)):
            ls[i] = ls[i] + s[i]
    string = ""
    for l in ls:
        string = string + l + "\n"
    return string
                
def octoPrint(notes):
    types = ()
    for n in notes:
        types = types + (n._type,)
    pnotes = ()
    for i in range(24):
        if i%12 in types:
            pnotes = pnotes + (pnote(i, True),)
        else:
            pnotes = pnotes + (pnote(i, False),)
    print(pstring(pnotes))
        
