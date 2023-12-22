# Assessing the Impact of Opioid Prescription Drug Policies on Mortality Trends

#### Collaborators - Jiayi Zhou, Jiechen Li, Ayush Gupta, Divya Sharma 

## Data
-  [Opioid prescribing rates](https://www.washingtonpost.com/national/2019/07/18/how-download-use-dea-pain-pills-database/?arc404=true) from DEA's Automatioin of Reports and Consolidated Orders System (ARCOS) detailing all transactional data of controlled substances sales by drug companies on a county level from 2006-2019
-  [Drug overdose mortality](https://www.dropbox.com/s/kad4dwebr88l3ud/US_VitalStatistics.zip?dl=0) counts from US National Vital Statistics System compressed mortality files for county-years 2003-2015
-  [County-level populations](https://wonder.cdc.gov/bridged-race-population.html) from CDC for rate denominators


## Methods

-  *Pre-post analysis*: Compare trends before and after policy changes
-  *Difference-in-difference models*: Contrast changes against demographically similar control states lacking interventions to isolate impact
-  Address missing mortality data using *imputation* process leveraging data properties to generate estimates suitable for advanced econometric analyses

## Outcomes

-  Opioid prescribing rates per capita
-  Drug overdose mortality rates

## Key Questions

-  How do implementations of prescription regulations affect the volume of opioids prescribed at the county level?
-  What is the impact of stricter opioid drug monitoring policies on overdose mortality rates?

## Test and Control States
The three test states examined in this analysis targeting prescriber practices are Florida, Texas, and Washington. Florida implemented stricter regulations and oversight on pain clinics along with enforcement crackdowns beginning in 2010. Texas expanded access controls for prescription drug monitoring in 2007 to reduce diversion and doctor shopping. Washington augmented requirements for frequent utilization checks and guidelines adherence in 2011 to impact prescribing decisions.

To account for underlying secular trends, neighboring states with highly aligned demographic, socioeconomic, and cultural profiles but lacking similar interventions in the given time period will provide control comparisons. Namely, these are Georgia, Alabama, and Tennessee for Florida policies; Oklahoma, Arkansas, and Louisiana for the Texas case; and Oregon and Idaho for Washington's regulations. The difference-in-difference design will contrast changes in outcomes in these aptly matched triplets against their test state to isolate the association between tightened restrictions and changes in opioid prescribing and mortality post-reform.






# Appendix

## Steps and Roadblocks

### Data Storage
Opioid Base Data for control states (Box) [link](https://duke.app.box.com/folder/233603607712?tc=collab-folder-invite-treatment-b)

### death_cleaning branch

1. 13 Nov. 2023 Jiechen: add ``US_VitalStatistics`` folder and ``state_death_clean_jiechen.ipynb`` file in ``10_Code``

2. 18 Nov. 2023 Jiechen: create a new branch named ``death_cleaning`` branch for death dataset only. Create ``death_clean.py`` under folder ``10_Code`` and delet the jupyther notebook. Finally, I met a issue in cleaning ``County Code`` that may need help. The issue I met here is that the "Deaths" column displaying zeros after the groupby operation. To effectively address this, I ensured that the data in the "Deaths" column is correctly interpreted as numeric and properly aggregated. This involves converting the "Deaths" column to a numeric format, accurately extracting state abbreviations, and then performing a groupby operation that groups by "Year", "County", and "State", followed by summing the deaths. By carefully following these steps, I aim to produce a DataFrame that accurately reflects drug-related deaths in each county and state for each year. However, if I included "County Code" in the grouping it would result no value (zero) in "Death". I have tried convert the data tpye to categorical, and find the unique County Code with zero death, and then try to do the groupby, but still failed.
