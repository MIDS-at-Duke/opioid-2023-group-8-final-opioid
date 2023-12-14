"""
The population data has been taken from https://wonder.cdc.gov/bridged-race-population.html
The data is in the form of tab-separated values, with additional info towards the end of the document, starting with the text "---"
We have downloaded the data from 1990 to 2010 separately, and then 2010 to 2020 separately, to maintain the file sizes and ensure complete download of data. We will combine the two in this code.
We will also remove the additional info at the end of the document while reading the file.
The raw downloaded data has been saved in the folder "00_raw_data" as "pop_1990_2010.txt" and "pop_2010_2020.txt" 
"""
# Importing libraries
import pandas as pd
import numpy as np

# Individual file links in the 00_raw_data folder
data_1990_2010 = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/population_cleaning/00_Source_Data/US_Pop_1990_2010.txt"
data_2010_2020 = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/population_cleaning/00_Source_Data/US_Pop_2010_2020.txt"

# Reading the file
# We will read the files in chunks of one line, and stop reading when we encounter the text "---"
df_1990_2010 = pd.DataFrame()
df_2010_2020 = pd.DataFrame()


def stop_reading(line):
    return "---" not in line


reader = pd.read_csv(data_1990_2010, iterator=True, chunksize=1, sep="\t")
for chunk in reader:
    if stop_reading(chunk.to_string()):
        df_1990_2010 = pd.concat([df_1990_2010, chunk])
    else:
        break

reader = pd.read_csv(data_2010_2020, iterator=True, chunksize=1, sep="\t")
for chunk in reader:
    if stop_reading(chunk.to_string()):
        df_2010_2020 = pd.concat([df_2010_2020, chunk])
    else:
        break

df_1990_2010.shape
# (66129, 8)

df_2010_2020.shape
# (31490, 8)

# Combining the two dataframes to get the entire 1990 to 2020 data in one dataframe
df_1990_2020 = pd.concat([df_1990_2010, df_2010_2020], ignore_index=True)
df_1990_2020.shape
# (97619, 8)

# Dropping the unnecessary Notes column
df_1990_2020 = df_1990_2020.drop("Notes", axis=1)
# Dropping the duplicated Yearly July 1st Estimates column
df_1990_2020 = df_1990_2020.drop("Yearly July 1st Estimates", axis=1)

# Renaming the Year column
df_1990_2020 = df_1990_2020.rename(columns={"Yearly July 1st Estimates Code": "Year"})

# Checking for duplicates at a state-county-year level
df_1990_2020[df_1990_2020[["State Code", "County Code", "Year"]].duplicated()].size
# Since the size is 0, there are no duplicates at a state-county-year level

# Changing data types according to requirements
df_1990_2020["Population"] = df_1990_2020["Population"].replace(
    "Missing", np.nan
)  # Replacing "Missing" with NaN
df_1990_2020["Population"] = df_1990_2020["Population"].astype(
    "float64"
)  # Changing the data type to float
df_1990_2020["State Code"] = df_1990_2020["State Code"].astype(
    "object"
)  # Changing the data type to object
df_1990_2020["County Code"] = df_1990_2020["County Code"].astype(
    "object"
)  # Changing the data type to object
df_1990_2020["Year"] = pd.to_datetime(
    df_1990_2020["Year"], format="%Y"
)  # Changing the data type to datetime

# Checking if there is missing data in Population for more than 1 year in a row for a state-county combination
grouped = df_1990_2020.sort_values("Year").groupby(["State Code", "County Code"])

missing_population = grouped.apply(
    lambda x: x["Population"].isnull().astype(int).diff().abs().max() > 1
)

missing_population[missing_population].shape
# (0,)

# Filling NA values in population based on interpolation of values from the same state-county from other years
df_1990_2020.sort_values("Year", inplace=True)

df_1990_2020["Population_filled"] = df_1990_2020["Population"]

df_1990_2020["Population_filled"] = df_1990_2020.groupby(["State Code", "County Code"])[
    "Population_filled"
].transform(lambda group: group.interpolate())
df_1990_2020.dropna(subset=["Population_filled"], inplace=True)

# df_1990_2020

# df_1990_2020[df_1990_2020["Population"].isnull()]

df_1990_2020[df_1990_2020["Population"].isnull()]["State"].value_counts()

# State
# Alaska      74
# Virginia    32

# Writing the dataframe to a readable csv file
df_1990_2020.to_csv("../20_Intermediate_Files/Cleaned_Population_Data.csv", index=False)
