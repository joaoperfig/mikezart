import musictheory as mt
import filezart as fz
import markovzart2

scale = mt.scale7()
cprog = (mt.chord3.fromScale(scale),mt.chord3.fromScale(scale),mt.chord3.fromScale(scale),mt.chord3.fromScale(scale))
progcount = 4
csize = 4

t = mt.theme(scale, cprog, progcount, csize)

inst = fz.getInfo()[0]
centre = mt.rselect(mt.listNotes(inst))
mtype = "chordic"

t.addVoice(inst, centre, mtype)
t.addVoice(inst, centre, mtype)

print(t.sortingString())

markovzart2.pooptest()
