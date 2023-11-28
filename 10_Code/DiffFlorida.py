# import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so
from matplotlib.lines import Line2D

pd.set_option("mode.copy_on_write", True)

# read in data
shipment = pd.read_csv("../20_Intermediate_Files/Florida_Merged.csv")

# subset the data for only the years needed
shipment_subset = shipment[["Year", "State Code", "County", "Population", "Dosage"]]
shipment_subset = shipment_subset[
    (shipment_subset["Year"] >= 2006) & (shipment_subset["Year"] <= 2013)
]

# add a calculation for shipments per capita
shipment_subset.loc[:, "ships_per_cap"] = (
    shipment_subset["Dosage"] / shipment_subset["Population"]
)

# subset the data for only FL
treatment_state = shipment_subset[shipment_subset["State Code"] == "FL"]
# subset the data for only the control states
controls = ["AL", "GA", "TN"]
control_states = shipment_subset[shipment_subset["State Code"].isin(controls)]


# specify the years needed before the policy change
year = [2006, 2007, 2008, 2009]
# create new dataframe with only data from those years
pre_FL_ship = treatment_state.loc[treatment_state["Year"].isin(year)]
post_FL_ship = treatment_state.loc[~treatment_state["Year"].isin(year)]
# control states
pre_crtl_ship = control_states.loc[control_states["Year"].isin(year)]
post_crtl_ship = control_states.loc[~control_states["Year"].isin(year)]


# define a function to plot the regression line and confidence interval
def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    years = list(np.arange(2006, 2013, 1))

    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    predictions["Treat"] = f"{legend}"

    # Plotting regression line
    plt.plot(predictions[xvar], predictions[yvar], color=color, label=legend)

    # Plotting confidence interval
    plt.fill_between(
        predictions[xvar],
        predictions["ci_low"],
        predictions["ci_high"],
        color=color,
        alpha=0.3,
        label=f"{legend} CI",
    )

    plt.xlabel(xvar)
    plt.ylabel("Presciptions per Capita")

    return predictions


# pre-post plot
# Create subplots
fig, ax = plt.subplots()

# Plot pre_FL_plot
pre_FL_plot = get_reg_fit(
    pre_FL_ship, "blue", "ships_per_cap", "Year", "FL", alpha=0.05
)

# Plot post_FL_plot
post_FL_plot = get_reg_fit(
    post_FL_ship, "blue", "ships_per_cap", "Year", "FL", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2010, color="black", linestyle="--", label="Policy Year")


plt.title("Pre-Post Analysis of Regulations on Opioid Prescriptions for Florida")

plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="FL"),
        Line2D([0], [0], color="grey", label="Control States"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.savefig("../20_Intermediate_Files/PrePostPrescriptionsFlorida.png")
plt.show()

# diff-in-diff plot
# Plot all data on the same chart
fig, ax = plt.subplots()

# Plot pre_FL_plot
pre_FL_plot = get_reg_fit(
    pre_FL_ship, "blue", "ships_per_cap", "Year", "FL", alpha=0.05
)

# Plot post_FL_plot
post_FL_plot = get_reg_fit(
    post_FL_ship, "blue", "ships_per_cap", "Year", "FL", alpha=0.05
)

# Plot pre_crtl_plot
pre_crtl_plot = get_reg_fit(
    pre_crtl_ship, "grey", "ships_per_cap", "Year", "Control States", alpha=0.05
)

# Plot post_crtl_plot
post_crtl_plot = get_reg_fit(
    post_crtl_ship, "grey", "ships_per_cap", "Year", "Control States", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2010, color="green", linestyle="--", label="Policy Year")

# Set chart title
plt.title("Diff-in-Diff Analysis of Regulations on Opioid Prescriptions for Florida")

# Display the legend with more specific labels
plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Florida"),
        Line2D([0], [0], color="grey", label="Control States"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.savefig("../20_Intermediate_Files/DiffPrescriptionsFlorida.png")
plt.show()
