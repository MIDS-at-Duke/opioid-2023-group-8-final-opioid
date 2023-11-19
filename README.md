# opioid-2023-group-8-final-opioid

opioid-2023-group-8-final-opioid created by GitHub Classroom

Base Data (Box) [link](https://duke.app.box.com/folder/233603607712?tc=collab-folder-invite-treatment-b)

## death_cleaning branch

1. 13 Nov. 2023 Jiechen: add ``US_VitalStatistics`` folder and ``state_death_clean_jiechen.ipynb`` file in ``10_Code``

2. 18 Nov. 2023 Jiechen: create a new branch named ``death_cleaning`` branch for death dataset only. Create ``death_clean.py`` under folder ``10_Code`` and delet the jupyther notebook. Finally, I met a issue in cleaning ``County Code`` that may need help. The issue I met here is that the "Deaths" column displaying zeros after the groupby operation. To effectively address this, I ensured that the data in the "Deaths" column is correctly interpreted as numeric and properly aggregated. This involves converting the "Deaths" column to a numeric format, accurately extracting state abbreviations, and then performing a groupby operation that groups by "Year", "County", and "State", followed by summing the deaths. By carefully following these steps, I aim to produce a DataFrame that accurately reflects drug-related deaths in each county and state for each year. However, if I included "County Code" in the grouping it would result no value (zero) in "Death". I have tried convert the data tpye to categorical, and find the unique County Code with zero death, and then try to do the groupby, but still failed.
