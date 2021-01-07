'''
Prototype for running the last created model
'''

import pickle
import pandas as pd

def convert(input, feature):
    if (feature in ["Altersgruppe", "FreeBedPercentage", "Notfallreserve"]):
        return float(t)
    else:
        return t

with open('./model.pkl', "rb") as pickle_file:
    model = pickle.load(pickle_file)

list_of_features = ["Bundesland", "Landkreis", "Altersgruppe", "Geschlecht", "FreeBedPercentage", "Notfallreserve"]

list_of_model_inputs = []

for feature in list_of_features:
    if feature == 'Altersgruppe':
        print("A00-A04 = 0\nA05-A14 = 1\nA15-A34 = 2\nA35-A59 = 3\nA60-A79 = 4\nA80+ = 5")
        t = input(feature + ": ")
    elif feature == "Geschlecht":
        t = input(feature + " (M/W): ")
    elif feature == "Bundesland":
        t = input(feature + " (Nordrhein-Westfalen): ")
    elif feature == "Landkreis":
        t = input(feature + " (LK Heinsberg): ")
    else:
        t = input(feature + ": ")

    list_of_model_inputs.append(convert(t, feature))

input_df = pd.DataFrame([list_of_model_inputs], columns=list_of_features)

print(input_df)

print("\nGiven Case will be a Deathcase: ", model.predict(input_df)[0])