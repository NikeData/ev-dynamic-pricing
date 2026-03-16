# This is a linear regression model that predicts ev charging demand (energy_sold_kwh)
#importing packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


#loading simulated charging data
df = pd.read_csv("ev_charging_data.csv")

# Feature Selection
#first drop datetime and session_id as they have no effect on energy sold
model_df = df.drop(columns= ['datetime', 'session_id'])

# Heat map to see colums that has high correlation with the demand (energy_sold_kwh)
plt.figure()
sns.heatmap(model_df.corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation Matrix")
plt.show()

# Multicollinearity can be observed between wholesale_price and retail_price, so whole_sale price will be dropped
model_df = model_df.drop(columns= 'wholesale_price')

# Then select the columns with the 5 best correlation as features
features = ['hour', 'is_weekend', 'temperature', 'retail_price', 'charging_sessions']
X = model_df[features]  
y = model_df['energy_sold_kwh']

# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("----------------------")
print(f'number of rows used in training model: {len(X_train)}')
print(f'number of rows for testing: {len(X_test)}')

# initialise linear model
model = LinearRegression()

#train model
model.fit(X_train, y_train)

#predict demand (energy_sold_kwh)
df["predicted_energy_sold_kwh"] = model.predict(X)

# Model Evaluation
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("R²:", r2)

# Feature Importance
coefficients = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_
})

print(coefficients)

# The regression coefficients indicate that charging demand (energy_sold_kwh) is primarily influenced by temporal patterns such as hour of day and weekend indicators, while retail electricity prices have a negative effect on demand due to price sensitivity.
# Saving Model
import joblib
joblib.dump(model, "demand_model.pkl")

# Predicted vs actual demand
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Demand (energy_sold_kwh)")
plt.ylabel("Predicted Demand (energy_sold_kwh)")
plt.title("Actual vs Predicted Charging Demand (energy_sold_kwh)")
plt.show()


df.to_csv('model.csv', index = False)


