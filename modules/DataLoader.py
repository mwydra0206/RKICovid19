"""
DataLoader Module for loading the covid19 dataset as wanted into the Jupyter Notebooks.
"""

# Needed imports
import pandas as pd
import numpy as np
import os

def load_covid19():
    """
    Standard loader of the covid19 Dataset.

    returning correct loaded covid19 dataframe.
    """

    # Importing with standard date formats
    covid19 = pd.read_csv("./data/rki_covid19_19_10_2020.csv", parse_dates=["Meldedatum", "Refdatum"], dayfirst=True, index_col="ObjectId")

    # Parsing own non-standard date format
    covid19["Datenstand"] = pd.to_datetime(covid19["Datenstand"], format="%d.%m.%Y, %H:%M Uhr", errors="ignore")

    # return DataFrame
    return covid19

def load_covid19_for_deathcase(features = None, label = "Deathcase", age_codes = None, cleaned=False):
    """
    Loader of the covid19 dataset for the deathcase classification.
    """

    covid19 = load_covid19()

    # Build up deathcases
    # -9 are the deathcase in the dataset
    covid19[label] = covid19["NeuerTodesfall"] != -9 

    if features is None:
         # Select needed features
        features = ["Bundesland", "Landkreis", "Altersgruppe", "Geschlecht", "Meldedatum", label]
    
    covid19 = covid19[features]

    # make ordinal feature
    if age_codes is None:
        # if age_codes is not set, then use standard definiton.
        age_codes = {
            "A00-A04" : 0, 
            "A05-A14" : 1, 
            "A15-A34" : 2, 
            "A35-A59" : 3, 
            "A60-A79" : 4, 
            "A80+" : 5, 
            "unbekannt": np.nan
        }

    # Convert the Age Group into defined format
    covid19["Altersgruppe"] = covid19["Altersgruppe"].apply(lambda x: age_codes[x])

    # covert "unbekannt" in "Geschlecht" to np.nan
    covid19["Geschlecht"] = covid19["Geschlecht"].apply(lambda x: np.nan if x == "unbekannt" else x)

    if cleaned:
        covid19 = covid19.dropna()

    return covid19, features
