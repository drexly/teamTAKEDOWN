import os
import glob

import scipy
import scipy.io.wavfile
from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=np.nan)

def plot_wav_fft(wav_filename, desc=None, trans=False):
    plt.clf()
    #plt.figure(num=None, figsize=(6, 4))
    sample_rate, X = scipy.io.wavfile.read(wav_filename)
    spectrum = fftpack.fft(X)
    freq = fftpack.fftfreq(len(X), d=1.0 / sample_rate)
    #print sample_rate,X,len(X)
    plt.subplot(211)
    num_samples =X.shape[0]
    plt.xlim(0, num_samples / sample_rate)
    plt.xlabel("time [s]")
    #plt.title(desc or wav_filename)
    fnarray=wav_filename.split("/")
    plt.title(fnarray[len(fnarray)-1])
    plt.plot(np.arange(num_samples) / sample_rate, X[:num_samples])
    plt.grid(True)

    if trans:
        plt.subplot(212)
        plt.xlim(0,1000)
        plt.xlabel("frequency [Hz]")
        #plt.xticks(np.arange(9) * 1000)
        #plt.xticks(np.arange(5) * 2000)
        if desc:
            desc = desc.strip()
            fft_desc = desc[0].lower() + desc[1:]
        else:
            fft_desc = wav_filename
        #plt.title("FFT of %s" % fft_desc)
        #plt.plot(freq, abs(spectrum), linewidth=1,color="red")
        #plt.plot(freq, abs(spectrum), color="red")
        plt.plot(freq, abs(spectrum), color="green")
        maxamplitude=np.amax(abs(spectrum[:]))
        for xy in zip(freq, abs(spectrum[:])):
            if maxamplitude==xy[1]:
                plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            #print xy
        plt.grid(True)
        plt.tight_layout()

    rel_filename = os.path.split(wav_filename)[1]
    #plt.savefig("%s_wav_fft.png" % os.path.splitext(rel_filename)[0], bbox_inches='tight')
    plt.show()

'''
def plot_wav_fft_demo():
    plot_wav_fft("sine_300.wav")
    plot_wav_fft("sine_10000.wav")
    plot_wav_fft("sine_mix.wav")

plot_wav_fft_demo()
'''
number_of_subplots=0
waves_array=[]

#for file in os.listdir("./AUDIO_DATA/JUNE_02_BACKGROUND/"):
for file in os.listdir("./AUDIO_DATA/JUNE_01_PHANTOMS/"):
    if file.endswith(".wav"):
        number_of_subplots+=1
        waves_array.append(file)

for i,j in enumerate(xrange(number_of_subplots)):
    file="./AUDIO_DATA/JUNE_01_PHANTOMS/"+waves_array[0]

    #file="./AUDIO_DATA/JUNE_02_BACKGROUND/"+waves_array[i]
    plot_wav_fft(file,None,True)
    break

