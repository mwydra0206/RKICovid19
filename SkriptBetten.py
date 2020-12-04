
import pandas as pd
import numpy as np
import os

df=pd.DataFrame

for i in range(1,17):
    covid19 = pd.read_csv("./data/intensivData/raw/{}-Beds.csv".format(i))
    infected=pd.read_csv("./data/intensivData/raw/{}-Infected.csv".format(i))
    covid19=covid19.merge(infected, left_on='date', right_on='date')
    covid19['IdBundesland']=i
    covid19.to_csv(r'./data/intensivData/{}-Sum.csv'.format(i), index= False, header=True)
    if(i==1):
        df=covid19
    else:
        df=df.append(covid19, ignore_index=True)
    print(df.head())


df=df.rename(columns={"Belegte Betten": "BelegteBetten", "Freie Betten": "FreieBetten", "COVID-19-Fälle": "COVID-19-Faelle"})
df.to_csv(r'./data/intensivData/bedsAndInfected.csv', index= False, header=True)