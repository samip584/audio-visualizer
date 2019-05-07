import pyaudio
import wave

import os
import sys
import timeit

import struct
import numpy as np
from scipy.fftpack import fft
import matplotlib as plt

plt.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
from tkinter import *



#import pandas as pd
# constants
CHUNK = int(1024 * 4)
FORMAT = pyaudio.paInt16 # has smth to do with bites per sec
CHANNELS = 1

# pygame.init()
root = Tk()
root.minsize(300,250)

#pygame.mixer.init()
#pygame.mixer.music.load("Johnny3.wav")
#pygame.mixer.music.play()


wf = wave.open("JohnnyTAOK.wav", 'rb')

total_frame = wf.getnframes()
total_cycle = total_frame/1024
RATE = wf.getframerate()
length = total_frame/RATE
print(length)
#pyaudio class instance
p = pyaudio.PyAudio()


# open stream 
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=RATE,
                output = True,
				frames_per_buffer = CHUNK
				)
data = wf.readframes(CHUNK)

fig = plt.figure.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)

x = np.linspace(0, RATE, int(CHUNK))
line, = ax.semilogx(x, np.random.rand(int(CHUNK)))
ax.set_xlim(20, RATE/2)
ax.get_xaxis().set_visible(False)
ax.yaxis.set_ticklabels([])
ax.set_yticklabels([])
ax.set_xticklabels([])

data = wf.readframes(CHUNK)
# play stream (3)
show = 0



while len(data) > 0:
	data = wf.readframes(CHUNK)
	new_data = np.fromstring(data, dtype=np.int16)  
	y_fft = fft(new_data)
	#data_int = np.concatenate((data_int, new_data))	
	stream.write(data)
	line.set_ydata(np.abs(y_fft[0:CHUNK])*2 / (10000 * CHUNK)) 
	#line.set_ydata(new_data)
	fig.canvas.draw()
	fig.canvas.flush_events()
	canvas.show()
	canvas.get_tk_widget().pack(fill = BOTH, expand = 1)





# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

root.mainloop()