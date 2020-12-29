import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from scipy.fftpack import fft

###Sine signal definition
def sine(A, f, N, phase):
    y = []
    global t
    t = np.arange(0, N / f, N / (1024 * f))
    for i in range(0, len(t)):
        y.append(A * np.sin(2 * np.pi * f * t[i] + phase))
    return t, y

## Generate sine signal
def generate():
    amp = int(ampEntry.get())
    freq = float(frequencyEntry.get())
    no_of_cycle = int(numEntry.get())
    global y
    t,y = sine(amp,freq * 1e9,no_of_cycle,(np.pi))
    plt.plot(t/1e-9,y)
    plt.xlabel('Time[ns]')
    plt.ylabel('Amplitude[V]')
    plt.title('Generated Signal')
    plt.show()

def fourier():
    # Creating frequency axis
    global scale_f,y_fft,freq_axis,N
    N = len(t)  # No of sample points
    Fs = 1 / (t[2] - t[1])  # Sampling Frequency
    freq_axis = np.arange(0, ((N / 2 - 1)) * (Fs / N), Fs / N)
    scale_f = 1e9
    # Frequency spectrum
    y_fft = 1/N *(fft(y,N))
    index = np.argmax(np.abs(y_fft[0:N // 2]))
    print("Frequency: " + str(freq_axis[index]))
    plt.plot(freq_axis/scale_f, np.abs(y_fft[0:N//2-1]))
    plt.ylabel("Amplitude[V]")
    plt.xlabel('Frequency[GHz]')
    plt.title('Frequency Spectrum')
    plt.show()

# Calculating phase spectrum
def phase():
    phase_source = np.angle(y_fft)
    #print(phase_source)
    plt.plot(freq_axis / scale_f, np.abs(phase_source[0:N // 2 - 1]))
    plt.ylabel("Phase[°]")
    plt.xlabel("Frequency[GHz]")
    plt.title('Phase Spectrum')
    plt.show()

# GUI framework
window = Tk()
window.title("Fourier Transform")
window.geometry("400x300")

freqLabel=Label(window, text="Frequency(in GHz):",font="Helvetica 12", height=3)
freqLabel.grid(column=0, row=1)

freq=StringVar(None)
frequencyEntry=Entry(window,textvariable=freq,width=5)
frequencyEntry.grid(column=1, row=1)

ampLabel=Label(window, text="Amplitude(in V):",font="Helvetica 12", height=3)
ampLabel.grid(column=0, row=2)

numLabel=Label(window, text="No of cycles:",font="Helvetica 12", height=3)
numLabel.grid(column=0, row=3)

phaseLabel=Label(window, text="Phase:",font="Helvetica 12", height=3)
phaseLabel.grid(column=0, row=4)

amp=StringVar(None)
ampEntry=Entry(window,textvariable=amp,width=5)
ampEntry.grid(column=1, row=2)

num=StringVar(None)
numEntry=Entry(window,textvariable=num,width=5)
numEntry.grid(column=1, row=3)

phi = ["π","π/2","π/4"]

phiOption = StringVar(window)
phiOption.set(phi[0]) # default value
piOption = OptionMenu(window, phiOption, *phi)
piOption.config(font="Helvetica 12")
piOption.grid(column=1, row=4)

buttonGen = Button(window, text="Generate", command = generate).grid( column=2, row=1)

buttonFourier = Button(window, text="Frequency Spectrum", command = fourier).grid( column=2, row=2)

buttonPhase =  Button(window, text="Phase Spectrum", command = phase).grid( column=2, row=3)
window.mainloop()