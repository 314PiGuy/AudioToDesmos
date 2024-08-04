import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import wave

#get some audio info
wav = wave.open('rick.wav', 'rb')
sampleRate = wav.getframerate()
samples = wav.getnframes()
duration = samples/sampleRate
#get an array of the audio amplitude at each sample (includes all channels)
signal = wav.readframes(samples)
signalArray = np.frombuffer(signal, dtype=np.int16)

lchannel = signalArray[0::2] #the amplitude array for only the left channel

times = np.linspace(0, duration, num=samples)
plt.figure(figsize=(15, 5))
plt.plot(times, lchannel)
plt.title('Amplitudes')
plt.ylabel('Signal value')
plt.xlabel('Time')
plt.xlim(0, duration)
plt.show()

#fourier transformation to get dominant frequencies
lchannelfft = fft(lchannel)
amplitudeSpectrum = np.abs(lchannelfft)
amplitudeSpectrum = amplitudeSpectrum / np.max(amplitudeSpectrum)
freqs = np.fft.fftfreq(samples, 1 / sampleRate)

plt.plot(freqs[:samples // 2], amplitudeSpectrum[:samples // 2])
plt.xlabel('Frequency')
plt.ylabel('Amplitude normalized')
plt.title('Dominant frequencies')
plt.show()

threshold = 0.2 #the threshold that the normalized frequencies have to be above to be considered dominant
dominant_freq_indices = np.where(amplitudeSpectrum[:samples // 2] >= threshold)[0]
dominant_freqs = freqs[dominant_freq_indices]

print(dominant_freqs)
