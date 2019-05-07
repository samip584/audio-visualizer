import pyaudio
import wave

import os
import sys
import time

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
CHUNK = 1024
FORMAT = pyaudio.paInt16 # has smth to do with bites per sec
CHANNELS = 1

# pygame.init()
root = Tk()
root.minsize(300,250)

pygame.mixer.init()
pygame.mixer.music.load("Johnny3.wav")
pygame.mixer.music.play()




wf = wave.open("Johnny3.wav", 'rb')

total_frame = wf.getnframes()
total_cycle = total_frame/1024

#pyaudio class instance
p = pyaudio.PyAudio()


# open stream 
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output = True,
				frames_per_buffer = CHUNK
				)
data = wf.readframes(CHUNK)

fig = plt.figure.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)

x = np.arange(0, int(CHUNK/2), 2)
line, = ax.plot(x, np.random.rand(int(CHUNK/4)))
ax.set_ylim(-250, 250)
ax.set_xlim(0, int(CHUNK/4))
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_yticklabels([])
ax.set_xticklabels([])

data = wf.readframes(CHUNK)
start_time = time.time()
# play stream (3)
show = 0
while len(data) > 0:
	data = wf.readframes(CHUNK)
	new_data = np.array(struct.unpack(str(CHUNK * 2) + 'B', data), dtype='b')[::8]
	#data_int = np.concatenate((data_int, new_data))
	if show == 1:
		line.set_ydata(new_data)
		fig.canvas.draw()
		fig.canvas.flush_events()
		canvas.show()
		canvas.get_tk_widget().pack(fill = BOTH, expand = 1)
	show = (show + 2)%3







# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

root.mainloop()