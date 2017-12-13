import scipy.io.wavfile
from scipy import io
import numpy
import sklearn
import os
from matplotlib.pyplot import  specgram
import matplotlib.pyplot as plt
from pylab import *

number_of_subplots=0
waves_array=[]

#for file in os.listdir("./AUDIO_DATA/JUNE_02_BACKGROUND/lbg/"):
for file in os.listdir("./AUDIO_DATA/JUNE_01_PHANTOMS/"):
    if file.endswith(".wav"):
        number_of_subplots+=1
        waves_array.append(file)

for i,j in enumerate(xrange(number_of_subplots)):
    file="./AUDIO_DATA/JUNE_01_PHANTOMS/"+waves_array[i]
    #file="./AUDIO_DATA/JUNE_02_BACKGROUND/lbg/"+waves_array[i]
    sample_rate, X = scipy.io.wavfile.read(file)
    print file, sample_rate, X.shape
    fft_features=abs(scipy.fft(X)[:])
    base_fn,ext=os.path.splitext(file)
    data_fn=base_fn+".fft"
    scipy.save(data_fn,fft_features)




