from numpy import mean, absolute
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import wave
import os

#get some audio info
wav = wave.open('rick.wav', 'rb')
sampleRate = wav.getframerate()
samples = wav.getnframes()
duration = samples / sampleRate

#get an array of the audio amplitude at each sample (includes all channels)
signalRaw = wav.readframes(samples)
signalArray = np.frombuffer(signalRaw, dtype=np.int16)

signal = signalArray[1::2]  #the amplitude array for only one channel

intervalTime = 0.1

interval = int(sampleRate * intervalTime)

def dominantFreq(signal):
  global interval
  #fourier transformation to get dominant frequencies
  signalfft = fft(signal)
  amplitudeSpectrum = np.abs(signalfft)
  if len(amplitudeSpectrum) == 0:
    return 0
  amplitudeSpectrum = amplitudeSpectrum / np.max(amplitudeSpectrum)
  freqs = np.fft.fftfreq(interval, 1 / sampleRate)
  return freqs[amplitudeSpectrum.argmax(axis=0)]

def IntervalFreqs():
  global signal, interval
  freqs = []
  start = 0
  while (start + interval <= len(signal)):
    section = signal[start:start + interval]
    freqs.append(dominantFreq(section))
    start += interval
  return freqs


freqs = IntervalFreqs()

def writeLine(data, start):
  count = 0
  with open('output.txt', 'a') as f:
    f.write(chr(count+65)+'\\left(x\\right)=\\left\\{')
    for time, freq in enumerate(data):
      f.write(f'{round(time*intervalTime+start, 2)}<x\\le{round((time+1)*intervalTime+start, 2)}:{round(freq, 2)}, \\ ')
  with open('output.txt', 'rb+') as f:
    f.seek(-4, os.SEEK_END)
    f.truncate()
  with open('output.txt', 'a') as f:
    f.write('\\right\\}\n')
  count+=1

writeLine(freqs, 0)
