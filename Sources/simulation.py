#importing packages
import pandas as pd
import numpy as np

# Since I do not have access to a live power grid's API, I are using physics and behavioral patterns (like peak hours and temperature) to "fake" a highly realistic dataset.

# Demand Data simulation
#setting random seed
np.random.seed(42)
# Create hourly timestamps for 120 days
dates = pd.date_range(start="2025-01-01", periods=24*120, freq="h")


#By extracting hour, day_of_week, and is_weekend, we are giving the Linear Regression model the primary "signals" it needs to find patterns in human behavior.
df = pd.DataFrame()
#df["session_id"] = pd.Series(np.arange(1, len(df) + 1)).values
df["datetime"] = dates
df["hour"] = df["datetime"].dt.hour
df["day_of_week"] = df["datetime"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5,6]).astype(int)

# Simulate temperature: Sine Wave is used to simulate the natural rise and fall of temperature over 24 hours.
# np.random.normal adds random noise to prevent over fitting, mean = 0, std = 1
# 25 + 5 sets the average temperature at 25 degree celcius, swinging between 20 and 30 degree celcius.
# 2*np.pi represents a full circle 360 degree or 2pi,df["hour"] / 24 scales 24-hour day into that circle.
#This creates a smooth curve that peaks during the day and falls at night.
df["temperature"] = 25 + 5*np.sin(2*np.pi*df["hour"]/24) + np.random.normal(0,1,len(df))

# Simulate wholesale electricity cost
#In a real-world energy market, prices don't follow a perfect, smooth curve. There are sudden micro-spikes or drops due to cloud cover affecting solar farms or a sudden surge in factory usage.
#Using a sine function to ensure that when the sun is down or people are waking up, the price fluctuates—just like a real energy market.
# $0.15 is the assumed base price, $0.05 represents price flunctuation throughout the day (+0.05 0r -0.05)
df["wholesale_price"] = (
    0.15 
    + 0.05*np.sin(2*np.pi*(df["hour"]+3)/24)
    + np.random.normal(0,0.01,len(df))
)
# customers deals with the retail price
df["retail_price"] = df["wholesale_price"] * 1.25
# Simulate base demand pattern
#Rush Hours (7-9 AM and 5-9 PM), mimics people charging their EVs when they get to work or when they get home
#peak effect will add 30 units of demand during peak hours, and only 10 during slow hours (like midnight)
peak_hours = df["hour"].between(7, 9) | df["hour"].between(17, 21)
peak_effect = np.where(peak_hours, 30, 10)
#df["peak_effect"] = 20 + 15*np.exp(-((df["hour"]-8)**2)/10) + 15*np.exp(-((df["hour"]-18)**2)/10)

weekend_effect = df["is_weekend"] * 2 #assumes demand spikes as people travel more on weekends, increasing charging needs.

# Number of Users (charging_sessions)
# Base sessions + peak boost + random noise
df["charging_sessions"] = (
    5 # Base number of cars
    + (peak_effect / 5) # Extra cars during rush hour
    + weekend_effect
    - (25 * df["retail_price"]) # High prices scare some users away
    + np.random.poisson(2, len(df)) # Random arrivals
).clip(lower=0).astype(int)  # clip(lower=0) ensures that the number of user is never negative

# Avg kWh per session (energy_per_session)
# Most EVs take 15-30 kWh for a quick charge, but we'll add some variance
#temperature affects the energy per session as it affects the battery efficiency
df["energy_per_session"] = (
    22 
    + 0.3 * (df["temperature"] - 25)  # temp effect
    + np.random.normal(0, 3, len(df))
).clip(lower=5)

#Calculate TOTAL DEMAND
df["energy_sold_kwh"] = df["charging_sessions"] * df["energy_per_session"]
df["energy_sold_kwh"] = df["energy_sold_kwh"].fillna(0)

# Reset the index, i want session id to start from 1
df = df.reset_index(drop=True)
# Insert session id at position 0
df.insert(0, 'session_id', np.arange(1, len(df) + 1))


#save df as csv
df.to_csv("ev_charging_data.csv", index=False)


#static pricing data simulation
import pandas as pd

# Loading the data frame we have after linear model
df = pd.read_csv('model.csv')

static_df = pd.DataFrame()
static_df["session_id"] = df['session_id']
static_df['static_markup_percent'] = 0.25 #25%
static_df["static_retail_price"] = df["wholesale_price"].mean() * 1.25  # using a 25% markup 
static_df["static_revenue"] = static_df["static_retail_price"] * df["predicted_energy_sold_kwh"]
static_df["static_cost"] = df["predicted_energy_sold_kwh"] * df["wholesale_price"]
static_df["static_profit"] = static_df["static_revenue"] - static_df["static_cost"]
static_df.to_csv('static_pricing_data.csv', index = False)
