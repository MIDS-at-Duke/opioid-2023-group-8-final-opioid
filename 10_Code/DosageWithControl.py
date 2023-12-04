"""Read and Handle the raw data, subset the data, calculate the dosage, and transform data"""
# Parse source data to parquet
# Note: All files has been parsed and upload to the Intermediate_Files Folder

import pandas as pd

pd.set_option("mode.copy_on_write", True)

# Read in raw data
# as raw data file is large for github, download data to local
# adjust the path to your local path
PATH = "../00_Source_Data/arcos_all_washpost.tsv"
csv_chunk = pd.read_table(PATH, chunksize=50_000, low_memory=False)

selected = []
for i, chunk in enumerate(csv_chunk):
    append_chunk = chunk.loc[
        (chunk["BUYER_STATE"] == "WA")
        | (chunk["BUYER_STATE"] == "TX")
        | (chunk["BUYER_STATE"] == "FL")
        | (chunk["BUYER_STATE"] == "OR")
        | (chunk["BUYER_STATE"] == "ID")
        | (chunk["BUYER_STATE"] == "OK")
        | (chunk["BUYER_STATE"] == "AR")
        | (chunk["BUYER_STATE"] == "LA")
        | (chunk["BUYER_STATE"] == "GA")
        | (chunk["BUYER_STATE"] == "AL")
        | (chunk["BUYER_STATE"] == "TN")
    ]
    selected.append(append_chunk)
data_selected = pd.concat(selected)

# modify and save to parquet file
data_selected["BUYER_STATE"].value_counts()
data_selected["NDC_NO"] = data_selected["NDC_NO"].astype(str)
data_selected.to_parquet("../20_Intermediate_Files/threeState.parquet")


# Subset, calculate dosage, and transform data
df = pd.read_parquet("../20_Intermediate_Files/threeState.parquet")

# subset data with columns needed
subset_df = df[
    [
        "BUYER_STATE",
        "BUYER_COUNTY",
        "TRANSACTION_DATE",
        "MME",
    ]
]

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

# Sum the dosage
subset_df["MME"] = subset_df.groupby(
    ["BUYER_STATE", "BUYER_COUNTY", "transaction_year"]
)["MME"].transform("sum")
subset_df = subset_df.drop_duplicates()

# Data overview
subset_df["MME"].describe()
subset_df["transaction_year"].value_counts()

# write to parquet file
subset_df.to_parquet("../20_Intermediate_Files/Dosage_FULL.parquet")
