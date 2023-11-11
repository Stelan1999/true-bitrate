#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uncomment for debugging:
#import matplotlib.pyplot as plt
import numpy
import soundfile
from scipy.fftpack import rfft
from scipy.io.wavfile import read
from scipy.signal.windows import hann
import sys
import warnings


def moving_average(a, w):
  # calculate moving average
  window = numpy.ones(int(w)) / float(w)
  r = numpy.convolve(a, window, 'valid')
  # len(a) = len(r) + w
  a = numpy.empty((int(w / 2)))
  a.fill(numpy.nan)
  b = numpy.empty((int(w - len(a))))
  b.fill(numpy.nan)
  # add nan arrays to equal input and output length
  return numpy.concatenate((a, r, b))


def find_cutoff(a, dx, diff, limit):
  for i in range(1, int(a.shape[0] - dx)):
    if a[-i] / a[-1] > limit:
      break
    if a[int(-i - dx)] - a[-i] > diff:
      return a.shape[0] - i - dx
  return a.shape[0]


# print usage if no argument given
if len(sys.argv[1:]) < 1:
  print('usage %s audio_file.wav' % (sys.argv[0]))
  sys.exit(1)

# read audio samples and ignore warnings, print errors
try:
  with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    input_data = soundfile.read(sys.argv[1])
except IOError as e:
  print(e[1])
  sys.exit(e[0])
#print(input_data[0])
#print(input_data[1])

# process data
freq = input_data[1]
audio = input_data[0]
channel = 0
samples = len(audio[:, 0])
seconds = int(samples / freq)
seconds = min(seconds, 30)
spectrum = [0] * freq

# run over the seconds (max 30)
for t in range(0, seconds - 1):
  # apply hanning window
  window = hann(freq)
  audio_second = audio[t * freq:(t + 1) * freq, channel] * window
  # do fft to add second to frequency spectrum
  spectrum += abs(rfft(audio_second))

# calculate average of the spectrum
spectrum /= seconds
# normalize frequency spectrum
spectrum = numpy.lib.scimath.log10(spectrum)
# smoothen frequency spectrum with window w
spectrum = moving_average(spectrum, freq / 100)
# find cutoff in frequency spectrum
cutoff = find_cutoff(spectrum, freq / 50, 1.25, 1.1)
# print bit rate of frequency spectrum before cutoff
print('%i kHz' % (cutoff / 2000))
print('(%s kHz)' % (cutoff / 2000.0))
if (cutoff // 2000) == 11:
  print('64 kbps')
elif (cutoff // 2000) == 16:
  print('128 kbps')
elif (cutoff // 2000) == 19:
  print('192 kbps')
elif (cutoff // 2000) == 20:
  print('320 kbps')
elif (cutoff // 2000) == 22:
  print('500 kbps')
elif (cutoff * 100) / freq > 90:
  print('lossless')
else:
  print("""
  11 kHz: 64 kbps
  16 kHz: 128 kbps
  19 kHz: 192 kbps
  20 kHz: 320 kbps
  22 kHz: 500 kbps
  """)

# debugging only:
if 'plt' in globals():
  # plot
  plt.plot(spectrum)
  # label the axes
  plt.ylabel('Magnitude')
  plt.xlabel('Frequency')
  # set the title
  plt.title('Spectrum')
  plt.axis((0, 45000, 0, 10))
  plt.show()
