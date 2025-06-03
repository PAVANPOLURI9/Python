import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson

# Step 1: Generate Random Dataset (Temperature vs Energy Consumption)
np.random.seed(42)
temperature = np.linspace(0, 40, 100)  # Temperature from 0°C to 40°C
true_weight = 2.5  # True weight in real life
true_bias = 5
noise = np.random.normal(0, 4, size=100)
energy_consumption = true_weight * temperature + true_bias + noise  # Actual data with noise

# Step 2: Define Single Neuron Function
def neuron(x, weight, bias):
    return weight * x + bias

# Step 3: Make Predictions Using Neuron (with slightly incorrect parameters)
predicted = neuron(temperature, weight=2.0, bias=3)

# Step 4: Plot Predicted vs Actual
plt.figure(figsize=(10, 5))
plt.scatter(temperature, energy_consumption, label="Actual", alpha=0.6)
plt.plot(temperature, predicted, color='red', label="Neuron Prediction (w=2.0, b=3)")
plt.xlabel("Temperature (°C)")
plt.ylabel("Energy Consumption (kWh)")
plt.title("Neuron Prediction vs Actual Data")
plt.legend()
plt.grid(True)
plt.show()

# Step 5: Calculate Squared Error (Loss)
loss = (predicted - energy_consumption)**2

# Step 6: Plot Loss Curve
plt.figure(figsize=(10, 5))
plt.plot(temperature, loss, label="Loss (Squared Error)", color="purple")
plt.xlabel("Temperature (°C)")
plt.ylabel("Loss")
plt.title("Loss Curve of Neuron Predictions")
plt.legend()
plt.grid(True)
plt.show()

# Step 7: Integration - Total Loss using Area Under the Curve
total_loss = simpson(loss, temperature)
print(f"✅ Total Integrated Loss (Area Under Loss Curve): {total_loss:.2f}")
