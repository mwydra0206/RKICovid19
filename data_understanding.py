# %% 

import pandas as pd

# Importing with standard date formats
covid19 = pd.read_csv("./data/rki_covid19_19_10_2020.csv", parse_dates=["Meldedatum", "Refdatum"], dayfirst=True)

# Parsing own non-standard date format
covid19["Datenstand"] = pd.to_datetime(covid19["Datenstand"], format="%d.%m.%Y, %H:%M Uhr", errors="ignore")

print(covid19.info())

covid19.head()


# %%

# covid19[covid19["Landkreis"].str.match("LK Heinsberg")]

genesen_gesamt = covid19[(covid19["NeuGenesen"] != -9) & (covid19["IdBundesland" == 5])]["NeuGenesen"].count()

# %%

tote_gesamt = covid19[covid19["NeuerTodesfall"] != -9]["NeuerTodesfall"].count()

# %%

covid19["ObjectId"].count() - genesen_gesamt - tote_gesamt

# %%

covid19[(covid19["NeuerTodesfall"] != -9) & (covid19["IdBundesland"] == 5)].count()

# %% 
print(genesen_gesamt / covid19["ObjectId"].count() * 100)
print(tote_gesamt / covid19["ObjectId"].count() * 100)

# %%

import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_theme(style="darkgrid")

sns.histplot(covid19["AnzahlTodesfall"], bins=100)

# %%
# Showing infections per day about the timeline

covid19_time = covid19[["Bundesland", "Meldedatum", "NeuerFall", "AnzahlFall"]]

# Letting all -1 cases out
covid19_time = covid19_time[covid19_time["NeuerFall"] != -1]

# Plotting the line
covid19_time.groupby(covid19_time["Meldedatum"]).sum()["AnzahlFall"].plot(linestyle='-')
plt.title("Infection cases per day")
plt.xlabel("Reporting date")
plt.ylabel("Count of cases")

# %%
# Showing deaths per day about the timeline

covid19_time = covid19[["Bundesland", "Meldedatum", "NeuerTodesfall", "AnzahlTodesfall"]]

# Letting all -1 cases out
covid19_time = covid19_time[(covid19_time["NeuerTodesfall"] != -1) & (covid19_time["NeuerTodesfall"] != -9)]

# Plotting the line
covid19_time.groupby(covid19_time["Meldedatum"]).sum()["AnzahlTodesfall"].plot(linestyle='-')
plt.title("Death per day")
plt.xlabel("Reporting date")
plt.ylabel("Count of deaths")

# %%
# Both Infection and Death per Day
covid19_time = covid19[["Bundesland", "Meldedatum", "NeuerFall", "AnzahlFall"]]

# Letting all -1 cases out
covid19_time = covid19_time[covid19_time["NeuerFall"] != -1]

# Plotting the line
covid19_time.groupby(covid19_time["Meldedatum"]).sum()["AnzahlFall"].plot(linestyle='-')

covid19_time = covid19[["Bundesland", "Meldedatum", "NeuerTodesfall", "AnzahlTodesfall"]]

# Letting all -1 cases out
covid19_time = covid19_time[(covid19_time["NeuerTodesfall"] != -1) & (covid19_time["NeuerTodesfall"] != -9)]

# Plotting the line
covid19_time.groupby(covid19_time["Meldedatum"]).sum()["AnzahlTodesfall"].plot(linestyle='-')

plt.title("Infection and Death per day")
plt.xlabel("Reporting date")
plt.ylabel("Count")
plt.legend(["Infection", "Death"])


# %%
# Showing infections in total for age group and sex

covid19_time = covid19[["Bundesland", "Geschlecht","Altersgruppe","NeuerFall", "AnzahlFall"]]

# Letting all -1 cases out
covid19_time = covid19_time[covid19_time["NeuerFall"] != -1]

# Plotting the line
sns.barplot(data=covid19_time.groupby(["Altersgruppe", "Geschlecht"]).sum().reset_index(["Altersgruppe","Geschlecht"]), x="Altersgruppe", y="AnzahlFall", hue="Geschlecht")

plt.title("Infection cases in total")
plt.xlabel("Age group")
plt.ylabel("Count of cases")
plt.legend(title="Sex")

# %%
# Showing infections in total for states

covid19_time = covid19[["Bundesland","NeuerFall", "AnzahlFall"]]

# Letting all -1 cases out
covid19_time = covid19_time[covid19_time["NeuerFall"] != -1]

# Plotting the line
sns.barplot(data=covid19_time.groupby("Bundesland").sum().reset_index(["Bundesland"]), x="Bundesland", y="AnzahlFall")

plt.title("Infection cases in total")
plt.xlabel("State")
plt.xticks(rotation=90)
plt.ylabel("Count of cases")

# %%
# Showing deaths in total for states

covid19_time = covid19[["Bundesland","NeuerTodesfall", "AnzahlTodesfall"]]

# Letting all -1 cases out
covid19_time = covid19_time[(covid19_time["NeuerTodesfall"] != -1) & (covid19_time["NeuerTodesfall"] != -9)]

# Plotting the line
sns.barplot(data=covid19_time.groupby("Bundesland").sum().reset_index(["Bundesland"]), x="Bundesland", y="AnzahlTodesfall")

plt.title("Deaths in total per state")
plt.xlabel("State")
plt.xticks(rotation=90)
plt.ylabel("Count of deaths")

# %%
# Showing deaths in total for age group and sex

covid19_time = covid19[["Altersgruppe", "Geschlecht","NeuerTodesfall", "AnzahlTodesfall"]]

# Letting all -1 cases out
covid19_time = covid19_time[(covid19_time["NeuerTodesfall"] != -1) & (covid19_time["NeuerTodesfall"] != -9)]

# Plotting the line
sns.barplot(data=covid19_time.groupby(["Altersgruppe", "Geschlecht"]).sum().reset_index(["Altersgruppe","Geschlecht"]), x="Altersgruppe", y="AnzahlTodesfall", hue="Geschlecht")

plt.title("Deaths cases in total per age group and sex")
plt.xlabel("Age group")
plt.ylabel("Count of death")
plt.legend(title="Sex")

# %%
tmp_pivot = covid19_time.groupby([covid19_time["Meldedatum"], "Bundesland"]).count()[["NeuerFall"]].reset_index(["Meldedatum", "Bundesland"])


# tmp_pivot

# tmp_pivot = tmp_pivot.groupby(tmp_pivot["Meldedatum"].dt.month).sum()

tmp_pivot.pivot(index="Meldedatum", columns="Bundesland", values="NeuerFall").plot()
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# %%

tmp_time_month = covid19_time.groupby(covid19_time["Meldedatum"].dt.month).count()
tmp_time_month["NeuerFall"].plot(linestyle='-')

# %%

tmp = covid19[["Bundesland", "NeuerTodesfall", "Geschlecht", "Altersgruppe"]
covid19_counts_state = tmp[(covid19["NeuerTodesfall"] != -9)]

# %%
# Count dead per state
plt.title("Count dead per state")
sns.countplot(x="Bundesland", data=covid19_counts_state)
plt.xticks(rotation=90)
plt.xlabel("State")
plt.ylabel("Count")

# %%
# Count dead per sex

plt.title("Count dead per sex")
sns.countplot(x="Geschlecht", data=covid19_counts_state)
plt.xlabel("Sex")
plt.ylabel("Count")

# %%
# Count dead per age group

plt.title("Count dead per age group")
sns.countplot(x="Altersgruppe", data=covid19_counts_state)
plt.xlabel("Age group")
plt.ylabel("Count")

# %%
