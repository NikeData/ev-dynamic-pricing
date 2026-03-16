# Dynamic EV charging prices will respond to this signals: reatail_price, demand (energy_sold_kwh), and peak hour
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dynamic_df = pd.read_csv('model.csv')
static_df = pd.read_csv('static_pricing_data.csv')



# Demand Multiplier (demand increases, price increases)
# Normalize demand
dynamic_df["normalized_demand"] = dynamic_df["predicted_energy_sold_kwh"] / dynamic_df["predicted_energy_sold_kwh"].max()

# Demand multiplier
dynamic_df["demand_multiplier"] = 1 + (dynamic_df["normalized_demand"] * 0.5) #Demand can increase price up to 50%.

# Peak hour multiplier
dynamic_df["time_multiplier"] = np.where(
    dynamic_df["hour"].between(17,21), 1.30,
    np.where(dynamic_df["hour"].between(7,9), 1.20, 1)
)

#adds 30% percent increase in price between (5 - 7) pm and 20% between (7-9) am.

# Calculate Dynamic price
dynamic_df["dynamic_price"] = (
    dynamic_df["retail_price"]
    * dynamic_df["demand_multiplier"]
    * dynamic_df["time_multiplier"]
)

# Apply Price Safety Limits.
# We don't want a drastic increase in price 

dynamic_df["dynamic_price"] = dynamic_df["dynamic_price"].clip(
    lower=dynamic_df["retail_price"] * 1.05,
    upper=dynamic_df["retail_price"] * 2
)
#the maximum price should not exceed retail_price * 2, and the minimum price should be a 5% increase

# Dynamic Pricing with demand elasticity
# we add a negative elasticity as some people will not react well to price increase
elasticity = -0.4   # negative demand elasticity, as increase in price might affect demand (energy_sold_kwh)
Price_change = (dynamic_df['dynamic_price']  - static_df['static_retail_price']) / static_df['static_retail_price']
dynamic_df['Adjusted_demand_kwh'] = dynamic_df['predicted_energy_sold_kwh'] * (1 + elasticity * Price_change)
dynamic_df['dynamic_revenue'] = dynamic_df['dynamic_price'] * dynamic_df['Adjusted_demand_kwh']  #revenue with elasticity
dynamic_df['dynamic_cost'] = dynamic_df['wholesale_price'] * dynamic_df['Adjusted_demand_kwh']
dynamic_df['dynamic_profit'] = dynamic_df['dynamic_revenue'] - dynamic_df['dynamic_cost']

print(f"dynamic_profit : {dynamic_df['dynamic_profit'].sum()}")


# Comparing static Profit with dynamic profit (profit with dynamic pricing)
# Profit increase percent
total_static_profit = static_df["static_profit"].sum()
total_dynamic_profit = dynamic_df["dynamic_profit"].sum()
profit_increase_percent = (
    (total_dynamic_profit - total_static_profit) 
    / total_static_profit
) * 100

print("Static Profit: $", round(total_static_profit,2))
print("Dynamic Profit: $", round(total_dynamic_profit,2))
print("Profit Increase:", round(profit_increase_percent,2), "%")


profits = [total_static_profit, total_dynamic_profit]
labels = ["Static Pricing", "Dynamic Pricing"]

plt.bar(labels, profits)
plt.ylabel("Total Profit ($)")
plt.title("Profit Comparison: Static vs Dynamic Pricing")

plt.show()

# The simulation showed a 90.52% profit increase under dynamic pricing. This large improvement occurs because the static pricing model applies a fixed 20% margin regardless of demand, while the dynamic pricing model adjusts prices during peak charging periods
