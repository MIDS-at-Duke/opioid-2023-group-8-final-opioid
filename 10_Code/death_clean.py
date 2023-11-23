import pandas as pd
import warnings

warnings.filterwarnings("ignore")
pd.set_option("mode.copy_on_write", True)

# list of 12 names for txt files from US_VitalStatistics.zip
file_names = [
    "Underlying%20Cause%20of%20Death%2C%202003",
    "Underlying%20Cause%20of%20Death%2C%202004",
    "Underlying%20Cause%20of%20Death%2C%202005",
    "Underlying%20Cause%20of%20Death%2C%202006",
    "Underlying%20Cause%20of%20Death%2C%202007",
    "Underlying%20Cause%20of%20Death%2C%202008",
    "Underlying%20Cause%20of%20Death%2C%202009",
    "Underlying%20Cause%20of%20Death%2C%202010",
    "Underlying%20Cause%20of%20Death%2C%202011",
    "Underlying%20Cause%20of%20Death%2C%202012",
    "Underlying%20Cause%20of%20Death%2C%202013",
    "Underlying%20Cause%20of%20Death%2C%202014",
    "Underlying%20Cause%20of%20Death%2C%202015",
]

# create a new list to contain combined data
data_frames = []

# states to select
selected_states = [", TX", ", FL", ", WA"]

github_base_url = "https://raw.githubusercontent.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/tree/death_cleaning/10_Code/"

# Filter out Alaska and "The Notes"
exclude_keywords = ["Alaska", "The Notes"]

for name in file_names:
    encoded_name = name.replace(" ", "%20") + ".txt"
    # construct the file path，you could change your path
    path = github_base_url + f"US_VitalStatistics/{encoded_name}.txt"
    # read txt file
    state_death = pd.read_csv(path, sep="\t")

    # Exclude rows containing Alaska and "The Notes"
    state_death = state_death[
        ~state_death["County"].str.contains("|".join(exclude_keywords))
    ]

    # Append to the list of dataframe
    data_frames.append(state_death)

combined_df = pd.concat(data_frames, ignore_index=True)
print(combined_df)

# check for missing values
missing_values = combined_df.isna().sum()
# print(missing_values)

# Convert 'Year' from float to categorical
combined_df["Year"] = combined_df["Year"].astype("category")

# Check the new data type
# print(combined_df["Year"].dtype)

# Convert 'County Code' to categorical
combined_df["County Code"] = combined_df["County Code"].astype("category")

# Check the new data type
# print(combined_df["County Code"].dtype)

# Filter Drug Related Deaths Only
# Filter for drug-related deaths
drug_related_causes = [
    "Drug poisonings (overdose) Unintentional (X40-X44)",
    "Drug poisonings (overdose) Suicide (X60-X64)",
    "All other drug-induced causes",
    "Drug poisonings (overdose) Undetermined (Y10-Y14)",
]

# Filter for drug-related deaths
drug_related_df = combined_df[
    combined_df["Drug/Alcohol Induced Cause"].isin(drug_related_causes)
]
# print(drug_related_df.head())


# Define a function to extract the state abbreviation
def extract_state(county_name):
    # Split the string by comma and take the last part as the state
    parts = county_name.split(", ")
    if len(parts) > 1:
        return parts[-1].strip()
    return None


# Apply the function to create a new 'State' column
drug_related_df["State"] = drug_related_df["County"].apply(extract_state)

# Convert "Deaths" to Numeric
drug_related_df["Deaths"] = pd.to_numeric(drug_related_df["Deaths"], errors="coerce")
drug_related_df["Deaths"].dtype


# Create a new df with Year, County, State, Drug-related Deaths
# Attention! I do not include County Code here, but I suppoesd to be.
# I write a explaination in README, and need your help.


# Define a function to extract the correct state abbreviation
def extract_correct_state(county_name):
    # Extract the state abbreviation from the county name
    parts = county_name.split(", ")
    if len(parts) > 1:
        return parts[-1].strip()
    return None


# Apply the function to create a new 'Correct_State' column
drug_related_df["Correct_State"] = drug_related_df["County"].apply(
    extract_correct_state
)

# Group by Year, County, and Correct_State, and sum the deaths
grouped_correct_df = (
    drug_related_df.groupby(["Year", "County", "County Code", "State"])["Deaths"]
    .sum()
    .reset_index()
)

# Check the grouped DataFrame
print(grouped_correct_df.sample(10))


# Filter for rows where both 'County' and 'State' columns indicate Washington State
wa_data = grouped_correct_df[
    (grouped_correct_df["County"].str.contains(", WA"))
    & (grouped_correct_df["Correct_State"] == "WA")
]

# Filter for Texas
tx_data = grouped_correct_df[
    (grouped_correct_df["County"].str.contains(", TX"))
    & (grouped_correct_df["Correct_State"] == "TX")
]

# Filter for Florida
fl_data = grouped_correct_df[
    (grouped_correct_df["County"].str.contains(", FL"))
    & (grouped_correct_df["Correct_State"] == "FL")
]
