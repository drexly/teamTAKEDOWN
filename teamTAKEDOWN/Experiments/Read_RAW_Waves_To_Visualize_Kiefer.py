import scipy.io.wavfile
from scipy import io
import numpy
import sklearn
import os
from matplotlib.pyplot import  specgram
import matplotlib.pyplot as plt
from pylab import *
'''
#wave_filename="m83.mp3"
wave_filename='./AUDIO_DATA/JUNE_01_PHANTOMS/P1_stationary.wav'
sample_rate, X= scipy.io.wavfile.read(wave_filename)
print sample_rate,X.shape
specgram(X, Fs=sample_rate)
plt.plot(X)
plt.show()
'''

number_of_subplots=0
waves_array=[]

#for file in os.listdir("./AUDIO_DATA/JUNE_02_BACKGROUND/"):
for file in os.listdir("./AUDIO_DATA/JUNE_01_PHANTOMS/"):
    if file.endswith(".wav"):
        number_of_subplots+=1
        waves_array.append(file)

subplots_adjust(hspace=1.000)
for i,j in enumerate(xrange(number_of_subplots)):
    file="./AUDIO_DATA/JUNE_01_PHANTOMS/"+waves_array[i]
    #file="./AUDIO_DATA/JUNE_02_BACKGROUND/"+waves_array[i]
    sample_rate, X = scipy.io.wavfile.read(file)
    print file, sample_rate, X.shape
    specgram(X, Fs=sample_rate)
    ax1 = plt.subplot(number_of_subplots,1,j+1)
    ax1.plot(X,color="green")
    ax1.set_title(waves_array[i],fontsize=10)
    if i<number_of_subplots-1:
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
    '''ax1.text(.5, .9, waves_array[i],
            horizontalalignment='center',
            transform=ax1.transAxes)'''
#plt.autoscale(enable=True, axis='both')
plt.show()




