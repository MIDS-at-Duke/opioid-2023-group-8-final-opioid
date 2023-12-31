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

data_2 = "https://github.com/MIDS-at-Duke/opioid-2023-group-8-final-opioid/raw/data_merging/20_Intermediate_Files/Florida_Merged.csv"

fl_and_control_death = pd.read_csv(data_2)

fl_and_control_death["Deaths"].sum()
# (60847.0)

# Dropping rows where there is any NA value
fl_and_control_death_cleaned = fl_and_control_death.dropna()

# Calculating death_per_capita
fl_and_control_death_cleaned["Death_per_capita"] = (
    fl_and_control_death_cleaned["Deaths"] / fl_and_control_death_cleaned["Population"]
)

# subset the data for only FL
fl_treatment_state = fl_and_control_death_cleaned[
    fl_and_control_death_cleaned["State Code"] == "FL"
]
# subset the data for only the control states
controls = ["KY", "OR", "TN"]
control_states = fl_and_control_death_cleaned[
    fl_and_control_death_cleaned["State Code"].isin(controls)
]

sub_fl_treatment_state = fl_treatment_state[
    (fl_treatment_state["Year"] >= 2006) & (fl_treatment_state["Year"] <= 2013)
]

sub_control_states = control_states[
    (control_states["Year"] >= 2006) & (control_states["Year"] <= 2013)
]

# specify the years needed before the policy change
year = [2006, 2007, 2008, 2009]
# create new dataframe with only data from those years
pre_FL_death = sub_fl_treatment_state.loc[sub_fl_treatment_state["Year"].isin(year)]
post_FL_death = sub_fl_treatment_state.loc[~sub_fl_treatment_state["Year"].isin(year)]

pre_crtl_death = sub_control_states.loc[sub_control_states["Year"].isin(year)]
post_crtl_death = sub_control_states.loc[~sub_control_states["Year"].isin(year)]


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
    plt.ylabel("Death per Capita")

    return predictions


# Create subplots
fig, ax = plt.subplots()

# Scale up the 'Death_per_capita' values by multiplying by 100000
pre_FL_death["Death_per_capita_scaled"] = pre_FL_death["Death_per_capita"] * 100000
post_FL_death["Death_per_capita_scaled"] = post_FL_death["Death_per_capita"] * 100000

# Plot pre_FL_plot
pre_FL_plot = get_reg_fit(
    pre_FL_death, "blue", "Death_per_capita_scaled", "Year", "Florida", alpha=0.05
)

# Plot post_FL_plot
post_FL_plot = get_reg_fit(
    post_FL_death, "blue", "Death_per_capita_scaled", "Year", "Florida", alpha=0.05
)

# Plotting a vertical line for the policy year
ax.axvline(x=2010, color="black", linestyle="--", label="Policy Year")

plt.title("Pre-Post Analysis of Regulations on Opioid Death for Florida")

plt.legend(
    handles=[
        Line2D([0], [0], color="blue", label="Florida"),
        Line2D([0], [0], color="green", linestyle="--", label="Policy Year"),
    ],
    loc="upper left",
)

# Show the plot
plt.subplots_adjust(left=0.17, right=0.95, top=0.95, bottom=0.1)
plt.savefig("PrePostDeathFlorida.png", format="png")
plt.show()

# Plot all data on the same chart
fig, ax = plt.subplots()

# Plot pre_FL_plot
pre_FL_plot = get_reg_fit(
    pre_FL_death, "blue", "Death_per_capita_scaled", "Year", "Florida", alpha=0.05
)

# Plot post_FL_plot
post_FL_plot = get_reg_fit(
    post_FL_death, "blue", "Death_per_capita_scaled", "Year", "Florida", alpha=0.05
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
ax.axvline(x=2010, color="green", linestyle="--", label="Policy Year")

# Set chart title
plt.title("Diff-in-Diff Analysis of Regulations on Opioid Deaths for Florida")

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
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
plt.savefig("DiffDeathFlorida.png", format="png")
plt.show()
