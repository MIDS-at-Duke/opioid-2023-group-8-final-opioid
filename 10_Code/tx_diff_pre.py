import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so
from matplotlib.lines import Line2D
import warnings

warnings.filterwarnings("ignore")
pd.set_option("mode.copy_on_write", True)

data_3 = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/data_merging/20_Intermediate_Files/Texas_Merged.csv"

tx_and_control_death = pd.read_csv(data_3)

tx_and_control_death["Deaths"].sum()
# (45420.0)

# Dropping rows where there is any NA value
tx_and_control_death_cleaned = tx_and_control_death.dropna()

# Calculating death_per_capita
tx_and_control_death_cleaned["Death_per_capita"] = (
    tx_and_control_death_cleaned["Deaths"] / tx_and_control_death_cleaned["Population"]
)

# subset the data for only TX
tx_treatment_state = tx_and_control_death_cleaned[
    tx_and_control_death_cleaned["State Code"] == "TX"
]
# subset the data for only the control states
controls = ["MO", "MN", "AR"]
control_states = tx_and_control_death_cleaned[
    tx_and_control_death_cleaned["State Code"].isin(controls)
]

sub_tx_treatment_state = tx_treatment_state[
    (tx_treatment_state["Year"] >= 2003) & (tx_treatment_state["Year"] <= 2010)
]

sub_control_states = control_states[
    (control_states["Year"] >= 2003) & (control_states["Year"] <= 2010)
]

# specify the years needed before the policy change
year = [2003, 2004, 2005, 2006]
# create new dataframe with only data from those years
pre_TX_death = sub_tx_treatment_state.loc[sub_tx_treatment_state["Year"].isin(year)]
post_TX_death = sub_tx_treatment_state.loc[~sub_tx_treatment_state["Year"].isin(year)]

pre_crtl_death = sub_control_states.loc[sub_control_states["Year"].isin(year)]
post_crtl_death = sub_control_states.loc[~sub_control_states["Year"].isin(year)]


def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    years = list(np.arange(2003, 2010, 1))

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
    plt.ylabel("Death per Capita")

    return predictions


# Create subplots
fig, ax = plt.subplots()

# Scale up the 'Death_per_capita' values by multiplying by 100000
pre_TX_death["Death_per_capita_scaled"] = pre_TX_death["Death_per_capita"] * 100000
post_TX_death["Death_per_capita_scaled"] = post_TX_death["Death_per_capita"] * 100000

# Plot pre_TX_plot
pre_TX_plot = get_reg_fit(
    pre_TX_death, "blue", "Death_per_capita_scaled", "Year", "Texas", alpha=0.05
)

# Plot post_TX_plot
post_TX_plot = get_reg_fit(
    post_TX_death, "blue", "Death_per_capita_scaled", "Year", "Texas", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2007, color="black", linestyle="--", label="Policy Year")

plt.title("Pre-Post Analysis of Regulations on Opioid Death for Texas")

plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Texas"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.savefig("PrePostDeathTexas.png", format="png")
plt.show()

# Plot all data on the same chart
fig, ax = plt.subplots()

# Plot pre_TX_plot
pre_TX_plot = get_reg_fit(
    pre_TX_death, "blue", "Death_per_capita_scaled", "Year", "Texas", alpha=0.05
)

# Plot post_TX_plot
post_TX_plot = get_reg_fit(
    post_TX_death, "blue", "Death_per_capita_scaled", "Year", "Texas", alpha=0.05
)


# Ensure the same scaling is applied to the control states dataframes
pre_crtl_death["Death_per_capita_scaled"] = pre_crtl_death["Death_per_capita"] * 100000
post_crtl_death["Death_per_capita_scaled"] = (
    post_crtl_death["Death_per_capita"] * 100000
)

# Plot pre_crtl_plot
pre_crtl_plot = get_reg_fit(
    pre_crtl_death,
    "grey",
    "Death_per_capita_scaled",
    "Year",
    "Control States",
    alpha=0.05,
)

# Plot post_crtl_plot
post_crtl_plot = get_reg_fit(
    post_crtl_death,
    "grey",
    "Death_per_capita_scaled",
    "Year",
    "Control States",
    alpha=0.05,
)

# Plotting a vertical line for the policy year
ax.axvline(x=2007, color="green", linestyle="--", label="Policy Year")

# Set chart title
plt.title("Diff-in-Diff Analysis of Regulations on Opioid Deaths for Texas")

# Display the legend with more specific labels
plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Texas"),
        Line2D([0], [0], color="grey", label="Control States"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.subplots_adjust(left=0.17, right=0.95, top=0.95, bottom=0.24)
plt.savefig("DiffDeathTexas.png", format="png")
plt.show()
