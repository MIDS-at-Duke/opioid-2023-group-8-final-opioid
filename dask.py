import os

# import client
from dask.distributed import Client

# Load Dask
import dask.dataframe as dd

client = Client()
client

# used in group project
cols_needed = [
    "BUYER_STATE",
    "BUYER_COUNTY",
    "TRANSACTION_DATE",
    "MME_Conversion_Factor",
    "CALC_BASE_WT_IN_GM",
    "MME",
]

opiod_project_df = dd.read_csv(
    "arcos_all_washpost.tsv",
    sep="\t",
    usecols=cols_needed,
)

opiod_project_df["Year"] = dd.to_datetime(
    opiod_project_df["TRANSACTION_DATE"], format="%Y-%m-%d"
).dt.year

opiod_project_df = (
    opiod_project_df.groupby(["BUYER_COUNTY", "BUYER_STATE", "Year"])["MME"]
    .sum()
    .reset_index()
)

output_df = opiod_project_df.compute()
