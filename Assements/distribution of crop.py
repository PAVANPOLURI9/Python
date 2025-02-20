import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm, uniform

# Sample Data for Green Chilli Yield (6 Acres, 2018-2024)
np.random.seed(42)

years = list(range(2018, 2025))  # 2018-2024 (inclusive)
acres = list(range(1, 7))  # 6 acres

data = []
for year in years:
    for acre in acres:
        data.append([year, acre])

df = pd.DataFrame(data, columns=["Year", "Acre"])

# **1. For 2018: Normal Distribution (Assume Mean=22 kN, Std Dev=2 kN)**
mean_2018 = 22  # Mean yield
std_dev_2018 = 2  # Standard deviation

df_2018 = df[df["Year"] == 2018]
df_2018["Yield (kN/acre)"] = norm.rvs(loc=mean_2018, scale=std_dev_2018, size=len(df_2018))

# **2. For 2019: Uniform Distribution (Assume Yield between 18 kN to 25 kN)**
low_2019 = 18  # Lower bound of uniform distribution
high_2019 = 25  # Upper bound of uniform distribution

df_2019 = df[df["Year"] == 2019]
df_2019["Yield (kN/acre)"] = uniform.rvs(loc=low_2019, scale=high_2019-low_2019, size=len(df_2019))

# **3. For 2020: Poisson Distribution (Assume lambda=20 for the Poisson process)**
lambda_2020 = 20  # Lambda for Poisson distribution (average yield)

df_2020 = df[df["Year"] == 2020]
df_2020["Yield (kN/acre)"] = poisson.rvs(mu=lambda_2020, size=len(df_2020))

# **Combine all the data for the years 2018-2020**
df_combined = pd.concat([df_2018, df_2019, df_2020])

# **Visualization of the Yields**
plt.figure(figsize=(12, 6))

# Histogram of Yield for 2018 (Normal Distribution)
plt.subplot(1, 3, 1)
plt.hist(df_2018["Yield (kN/acre)"], bins=10, color='blue', alpha=0.7)
plt.title('2018 Yield (Normal Distribution)')
plt.xlabel('Yield (kN/acre)')
plt.ylabel('Frequency')

# Histogram of Yield for 2019 (Uniform Distribution)
plt.subplot(1, 3, 2)
plt.hist(df_2019["Yield (kN/acre)"], bins=10, color='green', alpha=0.7)
plt.title('2019 Yield (Uniform Distribution)')
plt.xlabel('Yield (kN/acre)')
plt.ylabel('Frequency')

# Histogram of Yield for 2020 (Poisson Distribution)
plt.subplot(1, 3, 3)
plt.hist(df_2020["Yield (kN/acre)"], bins=10, color='red', alpha=0.7)
plt.title('2020 Yield (Poisson Distribution)')
plt.xlabel('Yield (kN/acre)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# **Output Results**
print("2018 Yield (Normal Distribution):")
print(df_2018[["Acre", "Yield (kN/acre)"]])

print("\n2019 Yield (Uniform Distribution):")
print(df_2019[["Acre", "Yield (kN/acre)"]])

print("\n2020 Yield (Poisson Distribution):")
print(df_2020[["Acre", "Yield (kN/acre)"]])
