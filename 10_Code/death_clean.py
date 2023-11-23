import pandas as pd
import requests
import zipfile
import io
import warnings

warnings.filterwarnings("ignore")
pd.set_option("mode.copy_on_write", True)

# URL pointing to the ZIP file in GitHub repository
github_zip_url = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/death_cleaning/00_Source_Data/US_VitalStatistics.zip"

# Filter out Alaska and "The Notes"
exclude_keywords = ["Alaska", "The Notes"]

data_frames = []

# Read the ZIP file from the URL
with requests.get(github_zip_url, stream=True) as r:
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        # List all files in the ZIP, excluding system files
        txt_files = [
            f
            for f in z.namelist()
            if f.endswith(".txt") and not f.startswith("__MACOSX")
        ]

        for file in txt_files:
            # Read each txt file
            with z.open(file) as f:
                try:
                    state_death = pd.read_csv(
                        f, sep="\t", encoding="latin1", on_bad_lines="skip"
                    )
                    # Filter out non-data rows
                    state_death = state_death.dropna(subset=["Deaths"])
                    # Check if 'County' column exists
                    if "County" in state_death.columns:
                        # Filter out rows with excluded keywords
                        state_death = state_death[
                            ~state_death["County"].str.contains(
                                "|".join(exclude_keywords), na=False
                            )
                        ]
                        data_frames.append(state_death)
                    else:
                        print(f"'County' column not found in file: {file}")
                except pd.errors.ParserError as e:
                    print(f"Error reading file {file}: {e}")
                    continue

# Combine all data frames
combined_df = pd.concat(data_frames, ignore_index=True)

# Drop "Notes"
combined_df = combined_df.drop("Notes", axis=1)

combined_df["Year"] = pd.to_datetime(combined_df["Year"], format="%Y").dt.strftime("%Y")

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
# drug_related_df.head()
drug_related_df["Deaths"] = pd.to_numeric(drug_related_df["Deaths"], errors="coerce")


# Define a function to extract the state abbreviation
def extract_state(county_name):
    # Split the string by comma and take the last part as the state
    parts = county_name.split(", ")
    if len(parts) > 1:
        return parts[-1].strip()
    return None


# Apply the function to create a new 'State' column
drug_related_df["State"] = drug_related_df["County"].apply(extract_state)
drug_related_df

# Remove state from county
drug_related_df["County"] = drug_related_df["County"].apply(lambda x: x.split(", ")[0])

# Groupby with Year, County Code, State, and Deaths
grouped_df_with_state = (
    drug_related_df.groupby(["Year", "County Code", "State"])["Deaths"]
    .sum()
    .reset_index()
)

print(grouped_df_with_state.sample(5))
