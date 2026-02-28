# Regulatory Risk Intelligence 
## Running the pipeline 
1. Place raw OCC data in 'data/raw/occ_enforcement.csv
2. Run: 

python -m src.preprocssing 

A cleaned dataset will be written to 'data/processed/'. 

A 200-row sample is included in 'data/sample/ for demonstration. 

##Limitations##
The model captures short-term enforcement momentum rather than structural bank risk.
Observations are monthly and may exhibit temporal dependence.
Macro-economic and regulatory regime variables are not yet included.
Model is intended for prioritization, not regulatory judgment.