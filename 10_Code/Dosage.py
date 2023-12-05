"""Read and Handle the raw data, subset the data, calculate the dosage, and transform data"""
# Parse source data to parquet
# Note: All files has been parsed and upload to the Intermediate_Files Folder

import pandas as pd

pd.set_option("mode.copy_on_write", True)

# Read in raw data
# as raw data file is large for github, download data to local
# adjust the path to your local path
PATH = "../00_Source_Data/arcos_all_washpost.tsv"
columns_subset = [
    "BUYER_STATE",
    "BUYER_COUNTY",
    "TRANSACTION_DATE",
    "MME_Conversion_Factor",
    "CALC_BASE_WT_IN_GM",
]
csv_chunk = pd.read_table(
    PATH, chunksize=50_000, usecols=columns_subset, low_memory=False
)

print("Data subset done.")

selected = []
for i, chunk in enumerate(csv_chunk):
    selected.append(chunk)
data_selected = pd.concat(selected)

print("Data selection done.")

# create a copy and perform data transformation
subset_df = data_selected.copy()

# Create year variable
# Convert the 'transaction_date' column to datetime format
subset_df["TRANSACTION_DATE"] = pd.to_datetime(subset_df["TRANSACTION_DATE"])
# Extract the year and create a new column 'transaction_year'
subset_df["transaction_year"] = subset_df["TRANSACTION_DATE"].dt.year
# Drop the original 'transaction_date' column
subset_df.drop(columns=["TRANSACTION_DATE"], inplace=True)

# Check NA values, find BUYER_COUNTY has NA values
subset_df.columns[subset_df.isnull().any()]
# Filter out NA values
subset_df = subset_df[subset_df["BUYER_COUNTY"].notna()]

# Calculate the morphine equivalent for each record
subset_df["MME"] = subset_df["MME_Conversion_Factor"] * subset_df["CALC_BASE_WT_IN_GM"]
# Drop the original 'MME_Conversion_Factor', 'CALC_BASE_WT_IN_GM' column
subset_df.drop(columns=["MME_Conversion_Factor", "CALC_BASE_WT_IN_GM"], inplace=True)

# Sum the dosage
subset_df["MME"] = subset_df.groupby(
    ["BUYER_STATE", "BUYER_COUNTY", "transaction_year"]
)["MME"].transform("sum")
subset_df = subset_df.drop_duplicates()

# Data overview
subset_df["MME"].describe()
subset_df["transaction_year"].value_counts()

# write to parquet file
subset_df.to_parquet("../20_Intermediate_Files/AllDosage.parquet")
