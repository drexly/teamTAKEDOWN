import requests
import os
url = 'http://127.0.0.1:5000/upload'
#files = {'file': open('UrbanSound8K/audio/fold1/7061-6-0-0.wav', 'rb')}
#files = {'file': open('C:\\Users\\drexly\\PycharmProjects\\TAKEDOWN\\2016-12-17-04-42-27.592000+00-15.wav', 'rb')}
#files = {'file': open('C:\\Users\\drexly\\PycharmProjects\\TAKEDOWN\\2016-12-17-04-42-23.257000+00-10.wav', 'rb')}
for i in range(0,142):
    files = {'file': open('C:\\Users\\drexly\\Desktop\\ee\\splitted\\'+str(i)+'.wav', 'rb')}
    r = requests.post(url, files=files)
    print(files['file'])
    print(r.text)
