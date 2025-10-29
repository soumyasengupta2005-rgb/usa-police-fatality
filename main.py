import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fatal_force = pd.read_csv(r"fatal-police-shootings-data.csv")
census = pd.read_csv(r"US-Census-Data.csv")

us_state_map = {
    'AL':'ALABAMA','AK':'ALASKA','AZ':'ARIZONA','AR':'ARKANSAS','CA':'CALIFORNIA',
    'CO':'COLORADO','CT':'CONNECTICUT','DE':'DELAWARE','FL':'FLORIDA','GA':'GEORGIA',
    'HI':'HAWAII','ID':'IDAHO','IL':'ILLINOIS','IN':'INDIANA','IA':'IOWA','KS':'KANSAS',
    'KY':'KENTUCKY','LA':'LOUISIANA','ME':'MAINE','MD':'MARYLAND','MA':'MASSACHUSETTS',
    'MI':'MICHIGAN','MN':'MINNESOTA','MS':'MISSISSIPPI','MO':'MISSOURI','MT':'MONTANA',
    'NE':'NEBRASKA','NV':'NEVADA','NH':'NEW HAMPSHIRE','NJ':'NEW JERSEY','NM':'NEW MEXICO',
    'NY':'NEW YORK','NC':'NORTH CAROLINA','ND':'NORTH DAKOTA','OH':'OHIO','OK':'OKLAHOMA',
    'OR':'OREGON','PA':'PENNSYLVANIA','RI':'RHODE ISLAND','SC':'SOUTH CAROLINA',
    'SD':'SOUTH DAKOTA','TN':'TENNESSEE','TX':'TEXAS','UT':'UTAH','VT':'VERMONT',
    'VA':'VIRGINIA','WA':'WASHINGTON','WV':'WEST VIRGINIA','WI':'WISCONSIN','WY':'WYOMING',
    'DC':'DISTRICT OF COLUMBIA'
}

fatal_force['state_full'] = fatal_force['state'].map(us_state_map)
census['state'] = census['state'].str.upper()
census['population'] = census['population'].fillna(0)

merged = pd.merge(fatal_force, census, left_on='state_full', right_on='state', how='left')

deaths_per_state = merged.groupby('state_full').size().sort_values(ascending=False)
deaths_by_race = merged.groupby('race').size().sort_values(ascending=False)
state_population = census.set_index('state')['population']

common_states = deaths_per_state.index.intersection(state_population.index)
deaths_per_state = deaths_per_state[common_states]
deaths_rate_per_state = deaths_per_state / state_population[common_states] * 100000

sns.set_style("whitegrid")
plt.figure(figsize=(12,6))
sns.barplot(x=deaths_per_state.index, y=deaths_per_state.values, palette="Reds_r", hue=None)
plt.xticks(rotation=90)
plt.ylabel("Number of Fatal Police Shootings")
plt.title("Fatal Police Shootings by State (2015-2024)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
sns.barplot(x=deaths_by_race.index, y=deaths_by_race.values, palette="Set2", hue=None)
plt.ylabel("Number of Fatal Police Shootings")
plt.title("Fatal Police Shootings by Race")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12,6))
sns.barplot(x=deaths_rate_per_state.index, y=deaths_rate_per_state.values, palette="Blues_r", hue=None)
plt.xticks(rotation=90)
plt.ylabel("Deaths per 100,000 population")
plt.title("Fatal Police Shootings Rate by State (2015-2024)")
plt.tight_layout()
plt.show()

print("Top 5 states by total fatal police shootings:")
print(deaths_per_state.head())
print("\nTop 5 states by death rate per 100k population:")
print(deaths_rate_per_state.sort_values(ascending=False).head())
print("\nFatal police shootings by race:")
print(deaths_by_race)
