import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Yield data per acre (kg) for each year
yield_data = {
    2018: [2200, 2300, 2100, 2250, 2180, 2220],
    2019: [2190, 2210, 2230, 2200, 2205, 2202],
    2020: [2100, 2150, 2200, 2180, 2225, 2175],
    2021: [2220, 2240, 2210, 2235, 2205, 2225],
    2022: [2250, 2260, 2245, 2235, 2220, 2240],
    2023: [2180, 2205, 2195, 2215, 2230, 2200],
    2024: [2200, 2215, 2220, 2240, 2235, 2210]
}

# Step 1: Calculate Mean, Median, Mode, Variance, Standard Deviation
stats_results = {}

for year, yields in yield_data.items():
    mean_yield = np.mean(yields)
    median_yield = np.median(yields)
    mode_yield = stats.mode(yields, keepdims=True).mode[0]
    variance_yield = np.var(yields, ddof=1)
    std_dev_yield = np.std(yields, ddof=1)

    stats_results[year] = {
        "Mean": mean_yield,
        "Median": median_yield,
        "Mode": mode_yield,
        "Variance": variance_yield,
        "Standard Deviation": std_dev_yield
    }

# Step 2: Print Mean, Median, Mode, Variance, Standard Deviation
print("Year-wise Statistical Analysis:\n")
for year, values in stats_results.items():
    print(f"Year {year}:")
    print(f"  Mean: {values['Mean']} kg/acre")
    print(f"  Median: {values['Median']} kg/acre")
    print(f"  Mode: {values['Mode']} kg/acre")
    print(f"  Variance: {values['Variance']:.2f}")
    print(f"  Standard Deviation: {values['Standard Deviation']:.2f}")
    print("-" * 40)

# Step 3: Probability Distributions (Normal, Uniform, Poisson)
years = [2018, 2019, 2020]

for year in years:
    plt.figure(figsize=(6, 4))
    yields = yield_data[year]

    if year == 2018:  # Normal Distribution
        mu, sigma = np.mean(yields), np.std(yields)
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        plt.plot(x, stats.norm.pdf(x, mu, sigma), label="Normal Distribution")
        plt.title(f"2018 Yield Distribution (Normal)")

    elif year == 2019:  # Uniform Distribution
        a, b = min(yields), max(yields)
        x = np.linspace(a, b, 100)
        plt.plot(x, stats.uniform.pdf(x, a, b-a), label="Uniform Distribution")
        plt.title(f"2019 Yield Distribution (Uniform)")

    elif year == 2020:  # Poisson Distribution
        lambda_val = np.mean(yields)
        x = np.arange(min(yields), max(yields)+1, 1)
        plt.plot(x, stats.poisson.pmf(x, lambda_val), marker="o", label="Poisson Distribution")
        plt.title(f"2020 Yield Distribution (Poisson)")

    plt.xlabel("Yield (kg/acre)")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid()
    plt.show()

# Step 4: Predict Future Yields (2025-2028)
past_means = [stats_results[year]["Mean"] for year in yield_data.keys()]
predicted_years = [2025, 2026, 2027, 2028]
future_predictions = {}

for i, year in enumerate(predicted_years):
    predicted_yield = past_means[-1] + (i * 5)  # Assuming a slight increase
    future_predictions[year] = predicted_yield

# Print Future Predictions
print("\nPredicted Yield for Future Years:")
for year, pred_yield in future_predictions.items():
    print(f"  {year}: {pred_yield:.2f} kg/acre")

# Step 5: Identify Highest and Lowest Yielding Land
avg_yields_per_acre = np.mean(list(yield_data.values()), axis=0)
highest_acre = np.argmax(avg_yields_per_acre) + 1
lowest_acre = np.argmin(avg_yields_per_acre) + 1

print("\nLand Productivity Analysis:")
print(f"  Highest Yielding Acre: Acre {highest_acre} with {avg_yields_per_acre[highest_acre-1]:.2f} kg/acre")
print(f"  Lowest Yielding Acre: Acre {lowest_acre} with {avg_yields_per_acre[lowest_acre-1]:.2f} kg/acre")

# Step 6: Plot Yields on Scale (1 to 5)
scaled_yield = (avg_yields_per_acre - np.min(avg_yields_per_acre)) / (np.max(avg_yields_per_acre) - np.min(avg_yields_per_acre)) * 4 + 1
plt.figure(figsize=(6, 4))
plt.bar(range(1, 7), scaled_yield, color='green', alpha=0.7)
plt.xticks(range(1, 7))
plt.xlabel("Land Plot")
plt.ylabel("Yield Scale (1 to 5)")
plt.title("Yield Scale (1 to 5) for Each Acre")
plt.grid()
plt.show()
