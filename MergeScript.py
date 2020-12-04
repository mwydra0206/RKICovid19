import pandas as pd
import numpy as np
import os

#Read the CSV, which contains the Number of Beds and Infected
bedsAndInfected=pd.read_csv("./data/intensivData/bedsAndInfected.csv", parse_dates=["date"],dayfirst=False)

#the attribute "date" is in datetime. I want to merge the data based on the date in the attribute "date"
bedsAndInfected['just_date']=pd.to_datetime(bedsAndInfected['date'], errors="ignore", utc=True).dt.date
bedsAndInfected=bedsAndInfected.drop(columns=['date'])

#parse the rki dataset
covid19Updated = pd.read_csv("./data/rki_covid19_04_12_2020.csv", parse_dates=["Meldedatum", "Refdatum"], dayfirst=False, index_col="ObjectId")
covid19 = pd.read_csv("./data/rki_covid19_19_10_2020.csv", parse_dates=["Meldedatum", "Refdatum"], dayfirst=False, index_col="ObjectId")


#do the same transformation from datetime to date with "refdatum" and call the new attribute just_date
covid19['just_date']=pd.to_datetime(covid19['Meldedatum'], errors="ignore", utc=True).dt.date
covid19Updated['just_date']=pd.to_datetime(covid19Updated['Meldedatum'], errors="ignore", utc=True).dt.date

#merge the data, where just_date is the same and the IdBundesland
#I used "left" so that to the rki data the correct data from bedsAndInfected will be added
covid19=pd.merge(covid19, bedsAndInfected, how='left', on=['just_date','IdBundesland'])
covid19=covid19.drop(columns=['just_date'])

covid19Updated=pd.merge(covid19Updated, bedsAndInfected, how='left', on=['just_date','IdBundesland'])
covid19Updated=covid19Updated.drop(columns=['just_date'])

covid19.to_csv(r'./data/intensivData/newRKI.csv', index= False, header=True)
covid19Updated.to_csv(r'./data/intensivData/newRkiUpdated.csv', index= False, header=True)
