import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set directory
directory = r"C:\AI\Python\cleaned_ipl_data_2020"

# Load specific CSV files
files = {
    "points_table": "cleaned_ipl2020_points_table.csv",
    "matches": "cleaned_ipl_2020_matches.csv",
    "ball_by_ball": "ipl_2020_ball_by_ball.csv"
}

dataframes = {}
for name, filename in files.items():
    file_path = os.path.join(directory, filename)
    try:
        print(f"Reading: {file_path}")
        dataframes[name] = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Print columns for debugging
for name, df in dataframes.items():
    print(f"\n{name.upper()} Columns: {df.columns.tolist()}")

# Declare the IPL 2020 Winner (only the winner, no opponent)
print("\nIPL 2020 Winner: Mumbai Indians")

# Visualization 1: Bar Plot - Total Runs Scored by Each Team (Points Table)
if "points_table" in dataframes and "Team" in dataframes["points_table"].columns and "Runs For" in dataframes["points_table"].columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dataframes["points_table"], x="Team", y="Runs For", hue="Team", palette="viridis", legend=False)
    plt.title("Total Runs Scored by Each Team (IPL 2020)", fontsize=14)
    plt.xlabel("Team", fontsize=12)
    plt.ylabel("Runs For", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualization 2: Box Plot - Runs Distribution by Winner (Matches)
if "matches" in dataframes and "winner" in dataframes["matches"].columns:
    # Assuming 'team1_score' or similar for runs; adjust based on printed columns
    runs_col = "Runs Against"  # Replace with actual column after checking output
    if runs_col in dataframes["matches"].columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=dataframes["matches"], x="winner", y=runs_col, hue="winner", palette="coolwarm", legend=False)
        plt.title("Runs Distribution by Winning Team (IPL 2020)", fontsize=14)
        plt.xlabel("Winning Team", fontsize=12)
        plt.ylabel(f"Runs ({runs_col})", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"\nWarning: '{runs_col}' not found in matches data. Skipping box plot. Check columns above.")

# Visualization 3: Histogram - Runs per Ball (Ball-by-Ball)
if "ball_by_ball" in dataframes and "runs" in dataframes["ball_by_ball"].columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(data=dataframes["ball_by_ball"], x="runs", bins=10, color="skyblue", kde=True)
    plt.title("Distribution of Runs per Ball (IPL 2020)", fontsize=14)
    plt.xlabel("Runs per Ball", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.tight_layout()
    plt.show()

# Visualization 4: Pie Chart - Match Win Distribution (Matches)
if "matches" in dataframes and "winner" in dataframes["matches"].columns:
    win_counts = dataframes["matches"]["winner"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(win_counts, labels=win_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    plt.title("Match Win Distribution by Team (IPL 2020)", fontsize=14)
    plt.tight_layout()
    plt.show()

print("\nVisualizations complete!")