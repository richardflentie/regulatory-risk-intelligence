# Regulatory Risk Intelligence 
## Running the pipeline 
1. Place raw OCC data in 'data/raw/occ_enforcement.csv
2. Run: 
python -m src.preprocssing 
A cleaned dataset will be written to 'data/processed/'. 
A 200-row sample is included in 'data/sample/ for demonstration. 

### Regulatory Risk Intelligence ###
A forward-looking risk model that predicts whether a bank will receive a regulatory enforcement action within the next 6 months. 

### Problem Statement ###
Regulatory enforcement actions often occur in clusters. Once a bank receives an enforcement action, it is more likely to experience additional actions in subsequent months. 
Risk teams need a structured way to prioritize monitroing resources. 
This project answers: 
Given historical enforcement activity, can we estimate the probability of a bank receiving another enforcement ation in the next 6 ths? 

### Data Used ###
* OCC enforcement action history data
* Monthly bank0level panel dataset
* Rolling 6-month event counts 
* Peer enforcement activity metrics
Each observation represents a: (bank,month)
The target variable: 
* y_next_6m = 1 
if enforcement occurs in the rolling 6 months
Time-based split was used to prevent lookahead bias. 

### Modeling Approach ###
events_last_6m -> bank-specific enforcement persistence 
peer_events_last_6m -> systemic regulatory activity 
Forward 6-month label construction
Time-based train/test validation 

Baseline model: 
Logistic Regression
No leakage
Imbalanced classification evaluation 

### Results ###
ROC-AUC:0.95
Top Decile Caputa ~92% 
Interpretation: If monitoring resources are focused on the top 10% highest-risk bank-months, approximately 92% of future events are captured. This indicates a strong clustering of regulatory risks. 

## Limitations ##
The model captures short-term enforcement momentum rather than structural bank risk.
Observations are monthly and may exhibit temporal dependence.
Macro-economic and regulatory regime variables are not yet included.
Model is intended for prioritization, not regulatory judgment.

### Why this project matters ###
Demonstrates: Time-series feature engineering
Forward-label construction 
Leakage Control 
Lift-based evaluation 
Modular Python analytics pipeline 

Application to operational risk, compliance analytics, and regulatory intelligence functions.

