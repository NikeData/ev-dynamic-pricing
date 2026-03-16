<<<<<<< HEAD
# EV Charging Dynamic Pricing System
Machine learning driven dynamic pricing system for EV charging stations.

#### Project Overview
This project develops a machine learning Dynamic pricing System for EV Charging Stations. The system predicts energy demand and adjusts charging prices dynamically to maximize profit while accounting for demand elasticity.

#### Business Problem
EV charging operators often apply a fixed markup (e.g., 25%). However, electricity demand and wholesale price fluctuates throughout the day,  can we dynamically adjust pricing to maximize profit?

#### Tools Used

Python (Pandas, NumPy, matplotlib, seaborn, Scikit-Learn)
PostgreSQL
Excel (Financial modeling)
Power BI (Dashboard)
Machine Learning (Linear Regression)


#### Architecture
Data Simulation → Demand Prediction → Dynamic Pricing → Financial Modeling → Dashboard

#### Methodology
Simulated hourly EV charging dataset (120 days),  
Built demand prediction model using Linear Regression,  
Derived price-demand function,  
Determined adjusted demand with respect to elasticity,  
Compared static vs dynamic pricing strategies,  
Sensitivity analysis,  
Visualized results in Power BI


#### Results
Dynamic pricing increased profit by 91%  
Identified peak pricing windows  
Average charging price: $0.24/kWh

