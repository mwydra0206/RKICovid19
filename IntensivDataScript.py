
import pandas as pd
import numpy as np
import os


def execute(dataSetNames):
    reCreateIntensivDataset()
    mergeIntensivWithRKI(dataSetNames)




def reCreateIntensivDataset():
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
        
    df=df.rename(columns={"Belegte Betten": "BelegteBetten", "Freie Betten": "FreieBetten", "COVID-19-Fälle": "COVID-19-Faelle"})
    df.to_csv(r'./data/intensivData/IntensivDataset.csv', index= False, header=True)


def mergeIntensivWithRKI(dataSetNames):
    #Read the CSV, which contains the Number of Beds and Infected
    bedsAndInfected=pd.read_csv("./data/intensivData/bedsAndInfected.csv", parse_dates=["date"],dayfirst=False)

    #the attribute "date" is in datetime. I want to merge the data based on the date in the attribute "date"
    bedsAndInfected['just_date']=pd.to_datetime(bedsAndInfected['date'], errors="ignore", utc=True).dt.date
    bedsAndInfected=bedsAndInfected.drop(columns=['date'])


    for index,name in enumerate(dataSetNames):
        
        #parse the rki dataset
        covid19 = pd.read_csv(name, parse_dates=["Meldedatum", "Refdatum"], dayfirst=False, index_col="ObjectId")

        #do the same transformation from datetime to date with "refdatum" and call the new attribute just_date
        covid19['just_date']=pd.to_datetime(covid19['Meldedatum'], errors="ignore", utc=True).dt.date

        #merge the data, where just_date is the same and the IdBundesland
        #I used "left" so that to the rki data the correct data from bedsAndInfected will be added
        covid19=pd.merge(covid19, bedsAndInfected, how='left', on=['just_date','IdBundesland'])
        covid19=covid19.drop(columns=['just_date'])

        covid19.to_csv(r'./data/intensivData/newRKI{}.csv'.format(index), index= False, header=True)



execute(["./data/rki_covid19_19_10_2020.csv","./data/rki_covid19_04_12_2020.csv"])