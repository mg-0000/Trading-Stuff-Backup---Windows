import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Load your dataset
# Example: dataset = pd.read_csv('path_to_your_dataset.csv')
# Ensure your dataset has the columns used as input variables like MA, BIAS, RSI, K, D, MACD, PSY, Volume, and the target variable (stock prices).
dataset = pd.read_csv('nifty_bank.csv')

# Define fuzzy variables
ma = ctrl.Antecedent(np.arange(0, 101, 1), 'ma')
bias = ctrl.Antecedent(np.arange(-10, 10, 0.1), 'bias')
rsi = ctrl.Antecedent(np.arange(0, 101, 1), 'rsi')
k = ctrl.Antecedent(np.arange(0, 101, 1), 'k')
d = ctrl.Antecedent(np.arange(0, 101, 1), 'd')
macd = ctrl.Antecedent(np.arange(-5, 5, 0.1), 'macd')
psy = ctrl.Antecedent(np.arange(0, 101, 1), 'psy')
volume = ctrl.Antecedent(np.arange(0, 1000000, 1000), 'volume')

# Define the output variable
price = ctrl.Consequent(np.arange(0, 101, 1), 'price')

# Membership functions
ma.automf(3)
bias.automf(3)
rsi.automf(3)
k.automf(3)
d.automf(3)
macd.automf(3)
psy.automf(3)
volume.automf(3)

price['low'] = fuzz.trimf(price.universe, [0, 0, 50])
price['medium'] = fuzz.trimf(price.universe, [0, 50, 100])
price['high'] = fuzz.trimf(price.universe, [50, 100, 100])

# Define rules
rule1 = ctrl.Rule(ma['poor'] & rsi['poor'], price['low'])
rule2 = ctrl.Rule(ma['average'] & rsi['average'], price['medium'])
rule3 = ctrl.Rule(ma['good'] & rsi['good'], price['high'])

# Add more rules as necessary
rule4 = ctrl.Rule(k['poor'] & d['poor'], price['low'])
rule5 = ctrl.Rule(k['average'] & d['average'], price['medium'])
rule6 = ctrl.Rule(k['good'] & d['good'], price['high'])
# ...

# Create control system and simulation
price_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
price_sim = ctrl.ControlSystemSimulation(price_ctrl)

# Example input data for prediction
def predict_stock_price(input_data):
    price_sim.input['ma'] = input_data['MA']
    price_sim.input['bias'] = input_data['BIAS']
    price_sim.input['rsi'] = input_data['RSI']
    price_sim.input['k'] = input_data['stochrsi_k']
    price_sim.input['d'] = input_data['stochrsi_d']
    price_sim.input['macd'] = input_data['MACD']
    price_sim.input['psy'] = input_data['PSY']
    price_sim.input['volume'] = input_data['Volume']
    price_sim.compute()
    return price_sim.output['Close']

# Split the dataset
X = dataset[['MA', 'BIAS', 'RSI', 'stochrsi_k', 'stochrsi_d', 'MACD', 'PSY', 'Volume']]
y = dataset['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and predict
predictions = [predict_stock_price(row) for _, row in X_test.iterrows()]

# Evaluate the model
mape = mean_absolute_percentage_error(y_test, predictions)
print(f'MAPE: {mape}')

# Note: This is a simplified example. The actual implementation might require fine-tuning of fuzzy sets and rules based on your specific dataset.
