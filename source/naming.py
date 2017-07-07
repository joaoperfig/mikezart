from random import random

def rselect(lista):
    dicti = {}
    for i in lista:
        dicti[i] = 1
    return wselect(dicti)

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

def firsters():
    return ('qu','wh','w','r','t','p','ph','s','sh','h','d','f','j','k','l','z','x','c','ch','v','b','n','m')

def addendums():
    return ('s','rt', 'st', 'nt', 'l', 'p', 't', 'n', 'm', 'f', 'ft', 'lt', 'ck', 'ght')

def intermediates():
    return ('m', 'n')

def mainers():
    return ('a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'au', 'ou', 'ea', 'ay', 'oy')

def uppercase(l):
    return l.upper()

def sylable():
    disp = {(0,1,0):1, (1,1,0):4, (0,1,1):1, (1,1,1):1}
    mode = wselect(disp)
    syl = ''
    if mode[0] == 1:
        syl = syl + rselect(firsters())
    if mode[1] == 1:
        syl = syl + rselect(mainers())
    if mode[2] == 1:
        syl = syl + rselect(intermediates())
    return syl
    
def endsyl():
    disp = {(0,1,0):1, (1,1,0):3, (0,1,1):0.5, (1,1,1):1}
    mode = wselect(disp)
    syl = ''
    if mode[0] == 1:
        syl = syl + rselect(firsters())
    if mode[1] == 1:
        syl = syl + rselect(mainers())
    if mode[2] == 1:
        syl = syl + rselect(addendums())
    return syl    

def singlename():
    disp = {1:2, 2:3, 3:2, 4:1}
    num = wselect(disp)
    name = ''
    for i in range(num-1):
        name = name + sylable()
    name = name + endsyl()
    name = uppercase(name[0]) + name[1:]
    return name

def name():
    disp = {1:2, 2:3, 3:2}
    num = wselect(disp)
    name = ""
    for i in range(num):
        name = name + singlename() + " "
    return name[:-1]