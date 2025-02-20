import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv("agriculture_data.csv")

# Set a style for better visualization
sns.set_style("whitegrid")

# --- Bar Chart: Average Yield per Crop ---
plt.figure(figsize=(8, 5))
sns.barplot(x="Crop", y="Yield (kg/acre)", data=df, estimator=lambda x: sum(x)/len(x))
plt.title("Average Yield per Crop")
plt.show()

# --- Line Chart: Yearly Yield Trend ---
plt.figure(figsize=(10, 5))
sns.lineplot(x="Year", y="Yield (kg/acre)", data=df, hue="Crop", marker="o")
plt.title("Yearly Yield Trend per Crop")
plt.show()

# --- Histogram: Yield Distribution ---
plt.figure(figsize=(8, 5))
sns.histplot(df["Yield (kg/acre)"], bins=20, kde=True)
plt.title("Yield Distribution")
plt.show()

# --- Pie Chart: Crop Distribution ---
plt.figure(figsize=(6, 6))
df["Crop"].value_counts().plot.pie(autopct="%1.1f%%", colors=["#ff9999","#66b3ff","#99ff99"])
plt.title("Crop Distribution")
plt.ylabel("")
plt.show()

# --- Scatter Plot: Rainfall vs Yield ---
plt.figure(figsize=(8, 5))
sns.scatterplot(x="Rainfall (mm)", y="Yield (kg/acre)",  data=df, hue="Crop", alpha=0.7)
plt.title("Rainfall vs Yield")
plt.show()

# --- Box Plot: Yield per Crop ---
plt.figure(figsize=(8, 5))
sns.boxplot(x="Crop", y="Yield (kg/acre)", data=df)
plt.title("Yield Distribution per Crop")
plt.show()

# --- Heat Map: Correlation between Factors ---
plt.figure(figsize=(8, 5))
numeric_df=df.select_dtypes(include="number")
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()

# --- Area Chart: Yield Trend ---
plt.figure(figsize=(10, 5))
df.groupby("Year")["Yield (kg/acre)"].sum().plot(kind="area", alpha=0.5, color="blue")
plt.title("Total Yield Over Years")
plt.xlabel("Year")
plt.ylabel("Total Yield")
plt.show()

# --- Violin Plot: Yield per Crop ---
plt.figure(figsize=(8, 5))
sns.violinplot(x="Crop", y="Yield (kg/acre)", data=df)
plt.title("Yield Distribution (Violin Plot)")
plt.show()

# --- Pair Plot: Relationship Between Variables ---
sns.pairplot(df, hue="Crop")
plt.show()
