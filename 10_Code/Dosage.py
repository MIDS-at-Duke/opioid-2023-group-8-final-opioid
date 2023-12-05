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
# define chunk size
chunk_size = 50_000

# create empty list to store the results
total_morphine_equivalents = []

# Process each chunk
for chunk in pd.read_csv(
    PATH,
    sep="\t",
    usecols=columns_subset,
    chunksize=chunk_size,
    low_memory=False,
):
    # Convert TRANSACTION_DATE to year
    chunk["Year"] = pd.to_datetime(chunk["TRANSACTION_DATE"], format="%Y-%m-%d").dt.year

    # Calculate the morphine equivalent for each record for milligrams
    chunk["MME"] = chunk["MME_Conversion_Factor"] * chunk["CALC_BASE_WT_IN_GM"] * 1000

    total_morphine_equivalents.append(chunk)

# Concatenate the results from all chunks
final_result = pd.concat(total_morphine_equivalents)

# Group by county, state, and year to ensure unique entries and sum if appearing multiple times
final_result = (
    final_result.groupby(["BUYER_COUNTY", "BUYER_STATE", "Year"])["MME"]
    .sum()
    .reset_index()
)

final_result.to_parquet("../20_Intermediate_Files/AllDosage.parquet")
