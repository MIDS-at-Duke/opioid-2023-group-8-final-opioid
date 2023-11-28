import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so
from matplotlib.lines import Line2D
import numpy as np
import statsmodels.formula.api as smf
import warnings

warnings.filterwarnings("ignore")
pd.set_option("mode.copy_on_write", True)

data_1 = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/data_merging/20_Intermediate_Files/Washington_Merged.csv"

wa_and_control_death = pd.read_csv(data_1)

# Calculating death_per_capita
wa_and_control_death["Death_per_capita"] = (
    wa_and_control_death["Deaths"] / wa_and_control_death["Population"]
)

wa_subset = wa_and_control_death[
    (wa_and_control_death["Year"] >= 2008) & (wa_and_control_death["Year"] <= 2015)
]

# subset the data for only WA
wa_treatment_state = wa_and_control_death[wa_and_control_death["State Code"] == "WA"]
# subset the data for only the control states
controls = ["OR", "OK", "ID"]
control_states = wa_and_control_death[wa_and_control_death["State Code"].isin(controls)]

wa_mean_deaths = wa_treatment_state["Death_per_capita"].mean()
# print("Mean of Death_per_capita:", wa_mean_deaths)
# print(wa_treatment_state.isnull().sum())
# Fill NaN values in the 'Death_per_capita' column with the mean value
wa_treatment_state["Death_per_capita"] = wa_treatment_state["Death_per_capita"].fillna(
    wa_mean_deaths
)

# Check if there are any NaN values left in the 'Death_per_capita' column
# print(wa_treatment_state["Death_per_capita"].isnull().sum())

# Estimate and fill the missing 'Deaths' values
wa_treatment_state.loc[wa_treatment_state["Deaths"].isnull(), "Deaths"] = (
    wa_treatment_state["Death_per_capita"] * wa_treatment_state["Population"]
)

control_mean_deaths = control_states["Death_per_capita"].mean()
# print("Mean of Death_per_capita in control_states:", control_mean_deaths)
control_states["Death_per_capita"] = control_states["Death_per_capita"].fillna(
    control_mean_deaths
)
# print(control_states["Death_per_capita"].isnull().sum())

# Estimate and fill the missing 'Deaths' values
control_states.loc[control_states["Deaths"].isnull(), "Deaths"] = (
    control_states["Death_per_capita"] * control_states["Population"]
)

sub_wa_treatment_state = wa_treatment_state[
    (wa_treatment_state["Year"] >= 2008) & (wa_treatment_state["Year"] <= 2015)
]

sub_control_states = control_states[
    (control_states["Year"] >= 2008) & (control_states["Year"] <= 2015)
]

# specify the years needed before the policy change
year = [2008, 2009, 2010, 2011]
# create new dataframe with only data from those years
pre_WA_death = sub_wa_treatment_state.loc[sub_wa_treatment_state["Year"].isin(year)]
post_WA_death = sub_wa_treatment_state.loc[~sub_wa_treatment_state["Year"].isin(year)]

pre_crtl_death = sub_control_states.loc[sub_control_states["Year"].isin(year)]
post_crtl_death = sub_control_states.loc[~sub_control_states["Year"].isin(year)]


def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    years = list(np.arange(2008, 2015, 1))

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

# Plot pre_WA_plot
pre_WA_plot = get_reg_fit(
    pre_WA_death, "blue", "Death_per_capita", "Year", "Washington", alpha=0.05
)

# Plot post_WA_plot
post_WA_plot = get_reg_fit(
    post_WA_death, "blue", "Death_per_capita", "Year", "Washington", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2012, color="black", linestyle="--", label="Policy Year")

plt.title("Pre-Post Analysis of Regulations on Opioid Death for Washington")

plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Washington"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.subplots_adjust(left=0.17, right=0.95, top=0.95, bottom=0.1)
plt.savefig("PrePostDeathWashington.pdf", format="pdf")
plt.show()

# Plot all data on the same chart
fig, ax = plt.subplots()

# Plot pre_WA_plot
pre_WA_plot = get_reg_fit(
    pre_WA_death, "blue", "Death_per_capita", "Year", "Washington", alpha=0.05
)

# Plot post_WA_plot
post_WA_plot = get_reg_fit(
    post_WA_death, "blue", "Death_per_capita", "Year", "Washington", alpha=0.05
)

# Plot pre_crtl_plot
pre_crtl_plot = get_reg_fit(
    pre_crtl_death, "grey", "Death_per_capita", "Year", "Control States", alpha=0.05
)

# Plot post_crtl_plot
post_crtl_plot = get_reg_fit(
    post_crtl_death, "grey", "Death_per_capita", "Year", "Control States", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2012, color="green", linestyle="--", label="Policy Year")

# Set chart title
plt.title("Diff-in-Diff Analysis of Regulations on Opioid Deaths for Washington")

# Display the legend with more specific labels
plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Washington"),
        Line2D([0], [0], color="grey", label="Control States"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
plt.savefig("DiffDeathWashington.pdf", format="pdf")
plt.show()
