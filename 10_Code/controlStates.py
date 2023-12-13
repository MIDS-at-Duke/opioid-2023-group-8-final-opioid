# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("mode.copy_on_write", True)

# Read the data
df = pd.read_parquet("AllDosage.parquet")

# Group the data by BUYER_STATE and Year, and calculate the mean MME for each group
grouped_data = df.groupby(["BUYER_STATE", "Year"])["MME"].mean().reset_index()

# Filter the data for fewer state
fewer_data = grouped_data[
    (grouped_data["BUYER_STATE"] == "TX")
    | (grouped_data["BUYER_STATE"] == "WA")
    | (grouped_data["BUYER_STATE"] == "FL")
    | (grouped_data["BUYER_STATE"] == "OH")
    | (grouped_data["BUYER_STATE"] == "MI")
    | (grouped_data["BUYER_STATE"] == "ME")
    | (grouped_data["BUYER_STATE"] == "KY")
    | (grouped_data["BUYER_STATE"] == "OR")
    | (grouped_data["BUYER_STATE"] == "ID")
    | (grouped_data["BUYER_STATE"] == "OK")
    | (grouped_data["BUYER_STATE"] == "AR")
    | (grouped_data["BUYER_STATE"] == "LA")
    | (grouped_data["BUYER_STATE"] == "GA")
    | (grouped_data["BUYER_STATE"] == "AL")
    | (grouped_data["BUYER_STATE"] == "TN")
    | (grouped_data["BUYER_STATE"] == "MO")
    | (grouped_data["BUYER_STATE"] == "MN")
    | (grouped_data["BUYER_STATE"] == "AR")
]

# Plot the trend for each BUYER_STATE
plt.figure(figsize=(12, 6))
for state in fewer_data["BUYER_STATE"].unique():
    state_data = fewer_data[fewer_data["BUYER_STATE"] == state]
    plt.plot(state_data["Year"], state_data["MME"], label=state)

# Add labels and legend
plt.xlabel("Year")
plt.ylabel("Mean MME")
plt.title("Trend of MME by Year for Each BUYER_STATE")
plt.legend()
plt.grid(True)
plt.show()

# Filter the data for Florida
FL_data = grouped_data[
    (grouped_data["BUYER_STATE"] == "FL")
    | (grouped_data["BUYER_STATE"] == "KY")
    | (grouped_data["BUYER_STATE"] == "TN")
    | (grouped_data["BUYER_STATE"] == "OR")
]

# Plot the trend for each BUYER_STATE
plt.figure(figsize=(12, 6))
for state in FL_data["BUYER_STATE"].unique():
    state_data = FL_data[FL_data["BUYER_STATE"] == state]
    plt.plot(state_data["Year"], state_data["MME"], label=state)

# Add labels and legend
plt.xlabel("Year")
plt.ylabel("Mean MME")
plt.title("Trend of MME by Year for Each BUYER_STATE")
plt.legend()
plt.grid(True)
plt.show()

# Filter the data for Washington
WA_data = grouped_data[
    (grouped_data["BUYER_STATE"] == "WA")
    | (grouped_data["BUYER_STATE"] == "OH")
    | (grouped_data["BUYER_STATE"] == "KY")
    | (grouped_data["BUYER_STATE"] == "ME")
]

# Plot the trend for each BUYER_STATE
plt.figure(figsize=(12, 6))
for state in WA_data["BUYER_STATE"].unique():
    state_data = WA_data[WA_data["BUYER_STATE"] == state]
    plt.plot(state_data["Year"], state_data["MME"], label=state)

# Add labels and legend
plt.xlabel("Year")
plt.ylabel("Mean MME")
plt.title("Trend of MME by Year for Each BUYER_STATE")
plt.legend()
plt.grid(True)
plt.show()

# Filter the data for Texas
TX_data = grouped_data[
    (grouped_data["BUYER_STATE"] == "TX")
    | (grouped_data["BUYER_STATE"] == "MO")
    | (grouped_data["BUYER_STATE"] == "MN")
    | (grouped_data["BUYER_STATE"] == "AR")
]

# Plot the trend for each BUYER_STATE
plt.figure(figsize=(12, 6))
for state in TX_data["BUYER_STATE"].unique():
    state_data = TX_data[TX_data["BUYER_STATE"] == state]
    plt.plot(state_data["Year"], state_data["MME"], label=state)

# Add labels and legend
plt.xlabel("Year")
plt.ylabel("Mean MME")
plt.title("Trend of MME by Year for Each BUYER_STATE")
plt.legend()
plt.grid(True)
plt.show()
