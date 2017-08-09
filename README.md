# mikezart

### about:
Mikezart is an autonomous music generator  
Mikezario is a tool for lazy musicians  

### setup:
- install ptython 3 or latter
- pip install pyaudio
- pip install pydub
- you may need to install audio codecs
- run "python3 mikezart2.py" or "python3 mikezario.py"

#### adding own instrument libraries:
- create a folder with your samples in /resources/
- create a text file named yourFolderName.mkzrt in /configuration/
- consult other .mkzrt files in /configuration/ for what to put inside your file

#### upcoming changes list:
- [x] Palette generator
- [ ] ~~Double note distribution~~ (will remain as it was to avoid problems of requesting too many notes)
- [x] Last note on note selection wil not be on same tempo 
- [x] tweights and mweights as arguments for voice.autoprogs 
- [x] add theme line sorting
- [ ] pallette and struct joiner 
- [ ] finish mikezario 
- [ ] finish mikezart 
