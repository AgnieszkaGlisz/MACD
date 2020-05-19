import jupyter
import pandas 
import csv
import matplotlib.pyplot as ptl
import numpy as np
from datetime import datetime

#N is the number of, next el in interation
def ema_n(i, prices,N) :
    alfa = 2/(N+1)
    q = 1 - alfa
    numerator = prices[i]
    denominator = 1
    for j in range(1,N):
        numerator+=(q*prices[i+j])
        denominator+=q
        q*= 1 - alfa

    return numerator/denominator

#Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie,Wolumen
file = pandas.read_csv("wig20.csv")

date = file['Data'].values
data = file['Zamknięcie'].values

counter = 0
max = len(file)
macd, signal = [], []

for i in range(counter, max -26):
    ema12 = ema_n(i,data,12)
    ema26 = ema_n(i,data,26)
    macd.append(ema12-ema26)

counter = 0
#srednia kroczaca
for i in range(counter, max-26-9):
    ema9 = ema_n(i,macd,9)
    signal.append(ema9)

ds,macd_s, data_s =[],[],[]
for i in range(0, len(signal)):
    ds.append(date[i])
    macd_s.append(macd[i])
    data_s.append(data[i])

current_price = data_s[0]
shares = round(current_price,0) #nr of actions
print("Your capital at the begining: 4000")
capital = 4000 
counter = 0
for i in range(1, len(data_s)):
    current_price = data_s[i]
    if ((macd_s[i] <= signal[i] and macd_s[i-1] >= signal[i-1]) or (macd_s[i] >= signal[i] and macd_s[i-1] <= signal[i-1])) :
        counter += 1
        if (macd_s[i-1] < signal[i-1] and counter > 3):
            counter = 0
            shares = round((capital/current_price),0)
            capital -= shares*current_price
        elif (macd_s[i-1] > signal[i-1] and counter > 3):
            counter = 0
            capital += shares*current_price
            shares = 0
    
print("Your capital now: ")
print(capital)

n_date = []
for da in date:
    datef = datetime.strptime(da,'%d/%m/%Y')
    n_date.append(datef)


fig = ptl.figure()
ax=ptl.subplot(111)
ax.plot(n_date[:len(macd)],macd, label='macd',linewidth=0.8)
ax.plot(n_date[:len(signal)],signal,label='signal', linewidth=0.8)
ptl.plot(n_date[:len(data)], data, label="Zamkniecie")
ptl.xlabel("Date")
ptl.title("Graph")
ptl.legend()
ptl.show