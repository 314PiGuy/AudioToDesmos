import madmom
import os
import wave

wav_path = 'pianorick.wav'

wav = wave.open(wav_path, 'rb')
duration = wav.getnframes()/wav.getframerate()
wav.close()

proc = madmom.features.NotePeakPickingProcessor(fps=100)
act = madmom.features.RNNPianoNoteProcessor()(wav_path)

noteEvents = proc(act)

frequencies = []
times = []

def midiToHz(m):
  return 440.0 * 2.0**((m-69)/12.0)

for note in noteEvents:
  time, pitch = note
  frequencies.append(midiToHz(pitch))
  times.append(time)


for i in range(1, len(frequencies)-1):
  dif = abs(frequencies[i]-frequencies[i-1])
  dif2 = abs(frequencies[i]-frequencies[i+1])
  if dif2 > 500 and dif > 500 and frequencies[i] > 1000:
    frequencies[i] = frequencies[i-1]


times.append(duration)

count = 0

def writeLine(start, num):
  global count
  with open('output.txt', 'a') as f:
    f.write(chr(count+65)+'\\left(x\\right)=\\left\\{')
    i = 0
    for i in range(start, start+num):
      f.write(f'{round(times[i], 3)}<x\\le{round(times[i+1], 3)}:{round(frequencies[i], 2)}, \\ ')
    ranges.append(times[i+1])
  with open('output.txt', 'rb+') as f:
    f.seek(-4, os.SEEK_END)
    f.truncate()
  with open('output.txt', 'a') as f:
    f.write('\\right\\}\n')
  count+=1


ranges = []

ranges.append(0)
start = 0

while (start + 200 <= len(frequencies)):
  writeLine(start, 200)
  start += 200
writeLine(start, len(frequencies)-start) 

with open('output.txt', 'a') as f:
  count = 0
  f.write('Z\\left(x\\right)=\\left\\{')
  for n in range(len(ranges)-1):
    f.write(f'{round(ranges[n], 2)}<x\\le{round(ranges[n+1], 2)}:{chr(65+count)}\\left(x\\right), \\ ')
    count+=1
with open('output.txt', 'rb+') as f:
  f.seek(-4, os.SEEK_END)
  f.truncate()
with open('output.txt', 'a') as f:
  f.write('\\right\\}\n')
  f.write('\\operatorname{tone}\\left(Z\\left(a\\right)\\right)\n')