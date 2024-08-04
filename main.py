from numpy import mean, absolute
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import wave

def dominantFreq(signal):
  #fourier transformation to get dominant frequencies
  signalfft = fft(signal)
  amplitudeSpectrum = np.abs(signalfft)
  amplitudeSpectrum = amplitudeSpectrum / np.max(amplitudeSpectrum)
  freqs = np.fft.fftfreq(samples, 1 / sampleRate)

  dominantFreqs = []
  threshold = 0.1
  #get the 3 most dominant frequencies
  while 1:
    dominantIndices = np.where(amplitudeSpectrum[:samples // 2] >= threshold)[0]
    dominantFreqs = freqs[dominantIndices]
    if (len(dominantFreqs) <= 3):
      break
    threshold += 0.01
  return dominantFreqs

def IntervalFreqs(signal, interval):
  freqs = []
  start = 0
  while (start + interval <= len(signal)):
    section = signal[start:start+interval]
    freqs.append(dominantFreq(section))
    start += interval
  return freqs

#get some audio info
wav = wave.open('rick.wav', 'rb')
sampleRate = wav.getframerate()
samples = wav.getnframes()
duration = samples/sampleRate
#get an array of the audio amplitude at each sample (includes all channels)
signal = wav.readframes(samples)
signalArray = np.frombuffer(signal, dtype=np.int16)

lchannel = signalArray[1::2] #the amplitude array for only the left channel

interval = int(sampleRate/10) #get the dominant frequencies every 0.1 seconds



freqs = IntervalFreqs(lchannel, interval)
