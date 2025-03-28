import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the data
# If you have the data in a CSV file, use this:
# csv_file = "ipl_2020_matches.csv"
# df = pd.read_csv(csv_file)

# Alternatively, load the data directly as a DataFrame
data = {
    "date": [
        "2020-09-19", "2020-09-20", "2020-09-21", "2020-09-22", "2020-09-23", "2020-09-24", "2020-09-25",
        "2020-09-26", "2020-09-27", "2020-09-28", "2020-09-29", "2020-09-30", "2020-10-01", "2020-10-02",
        "2020-10-03", "2020-10-03", "2020-10-04", "2020-10-04", "2020-10-05", "2020-10-06", "2020-10-07",
        "2020-10-08", "2020-10-09", "2020-10-10", "2020-10-10", "2020-10-11", "2020-10-11", "2020-10-12",
        "2020-10-13", "2020-10-14", "2020-10-15", "2020-10-16", "2020-10-17", "2020-10-17", "2020-10-18",
        "2020-10-18", "2020-10-19", "2020-10-20", "2020-10-21", "2020-10-22", "2020-10-23", "2020-10-24",
        "2020-10-24", "2020-10-25", "2020-10-25", "2020-10-26", "2020-10-27", "2020-10-28", "2020-10-29",
        "2020-10-30", "2020-10-31", "2020-10-31", "2020-11-01", "2020-11-01", "2020-11-02", "2020-11-03",
        "2020-11-05", "2020-11-06", "2020-11-08", "2020-11-10"
    ],
    "match": [
        "MI VS CSK, 1ST MATCH", "DC VS KXIP, 2ND MATCH", "RCB VS SRH, 3RD MATCH", "RR VS CSK, 4TH MATCH",
        "MI VS KKR, 5TH MATCH", "KXIP VS RCB, 6TH MATCH", "DC VS CSK, 7TH MATCH", "SRH VS KKR, 8TH MATCH",
        "KXIP VS RR, 9TH MATCH", "RCB VS MI, 10TH MATCH", "SRH VS DC, 11TH MATCH", "KKR VS RR, 12TH MATCH",
        "MI VS KXIP, 13TH MATCH", "SRH VS CSK, 14TH MATCH", "RR VS RCB, 15TH MATCH", "DC VS KKR, 16TH MATCH",
        "MI VS SRH, 17TH MATCH", "KXIP VS CSK, 18TH MATCH", "DC VS RCB, 19TH MATCH", "MI VS RR, 20TH MATCH",
        "KKR VS CSK, 21ST MATCH", "SRH VS KXIP, 22ND MATCH", "DC VS RR, 23RD MATCH", "KKR VS KXIP, 24TH MATCH",
        "RCB VS CSK, 25TH MATCH", "SRH VS RR, 26TH MATCH", "DC VS MI, 27TH MATCH", "RCB VS KKR, 28TH MATCH",
        "CSK VS SRH, 29TH MATCH", "DC VS RR, 30TH MATCH", "RCB VS KXIP, 31ST MATCH", "KKR VS MI, 32ND MATCH",
        "RR VS RCB, 33RD MATCH", "CSK VS DC, 34TH MATCH", "KKR VS SRH, 35TH MATCH", "MI VS KXIP, 36TH MATCH",
        "CSK VS RR, 37TH MATCH", "DC VS KXIP, 38TH MATCH", "KKR VS RCB, 39TH MATCH", "RR VS SRH, 40TH MATCH",
        "CSK VS MI, 41ST MATCH", "KKR VS DC, 42ND MATCH", "KXIP VS SRH, 43RD MATCH", "RCB VS CSK, 44TH MATCH",
        "MI VS RR, 45TH MATCH", "KKR VS KXIP, 46TH MATCH", "SRH VS DC, 47TH MATCH", "RCB VS MI, 48TH MATCH",
        "KKR VS CSK, 49TH MATCH", "KXIP VS RR, 50TH MATCH", "DC VS MI, 51ST MATCH", "RCB VS SRH, 52ND MATCH",
        "KXIP VS CSK, 53RD MATCH", "KKR VS RR, 54TH MATCH", "RCB VS DC, 55TH MATCH", "MI VS SRH, 56TH MATCH",
        "MI VS DC, QUALIFIER 1", "RCB VS SRH, ELIMINATOR", "DC VS SRH, QUALIFIER 2", "DC VS MI, FINAL"
    ],
    "winner": [
        "CSK", "TIE", "RCB", "RR", "MI", "KXIP", "DC", "KKR", "RR", "TIE", "SRH", "KKR", "MI", "SRH", "RCB",
        "DC", "MI", "CSK", "DC", "MI", "KKR", "SRH", "DC", "KKR", "RCB", "RR", "MI", "RCB", "CSK", "DC", "KXIP",
        "MI", "RCB", "DC", "TIE", "TIE", "RR", "KXIP", "RCB", "SRH", "MI", "KKR", "KXIP", "CSK", "RR", "KXIP",
        "SRH", "MI", "CSK", "RR", "MI", "SRH", "CSK", "KKR", "DC", "SRH", "MI", "SRH", "DC", "MI"
    ],
    "loser": [
        "MI", "TIE", "SRH", "CSK", "KKR", "KXIP", "CSK", "SRH", "KXIP", "TIE", "DC", "RR", "KXIP", "CSK", "RR",
        "KKR", "SRH", "KXIP", "RCB", "RR", "CSK", "KXIP", "RR", "KXIP", "CSK", "SRH", "DC", "KKR", "SRH", "RR",
        "RCB", "KKR", "RR", "CSK", "TIE", "TIE", "CSK", "DC", "KKR", "RR", "CSK", "DC", "KXIP", "RCB", "MI", "KKR",
        "DC", "RCB", "KKR", "KXIP", "DC", "RCB", "KXIP", "RR", "RCB", "MI", "DC", "RCB", "SRH", "DC"
    ],
    "place": [
        "ABU DHABI", "DUBAI", "DUBAI", "SHARJAH", "ABU DHABI", "DUBAI", "DUBAI", "ABU DHABI", "SHARJAH", "DUBAI",
        "ABU DHABI", "DUBAI", "ABU DHABI", "DUBAI", "ABU DHABI", "SHARJAH", "SHARJAH", "DUBAI", "DUBAI", "ABU DHABI",
        "ABU DHABI", "DUBAI", "SHARJAH", "ABU DHABI", "DUBAI", "DUBAI", "ABU DHABI", "SHARJAH", "DUBAI", "DUBAI",
        "SHARJAH", "ABU DHABI", "DUBAI", "SHARJAH", "ABU DHABI", "DUBAI", "ABU DHABI", "DUBAI", "ABU DHABI", "DUBAI",
        "SHARJAH", "ABU DHABI", "DUBAI", "DUBAI", "ABU DHABI", "SHARJAH", "DUBAI", "ABU DHABI", "DUBAI", "ABU DHABI",
        "DUBAI", "SHARJAH", "ABU DHABI", "DUBAI", "ABU DHABI", "SHARJAH", "DUBAI", "ABU DHABI", "ABU DHABI", "DUBAI"
    ],
    "stage": [
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE",
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE",
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE",
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE",
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE",
        "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "LEAGUE", "QUALIFIER 1", "ELIMINATOR", "QUALIFIER 2", "FINAL"
    ]
}

df = pd.DataFrame(data)

# Step 2: Data Preprocessing
# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Replace team abbreviations with full names for better readability
team_mapping = {
    "MI": "Mumbai Indians",
    "CSK": "Chennai Super Kings",
    "DC": "Delhi Capitals",
    "KXIP": "Punjab Kings",
    "RCB": "Royal Challengers Bangalore",
    "SRH": "Sunrisers Hyderabad",
    "RR": "Rajasthan Royals",
    "KKR": "Kolkata Knight Riders",
    "TIE": "Tie"
}
df["winner"] = df["winner"].map(team_mapping)
df["loser"] = df["loser"].map(team_mapping)

# Step 3: Visualization 1 - Bar Chart: Number of Wins per Team
# Count wins per team (excluding ties from the win count)
win_counts = df[df["winner"] != "Tie"]["winner"].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=win_counts.values, y=win_counts.index, hue=win_counts.index, palette="viridis", legend=False)
plt.title("IPL 2020: Number of Wins per Team", fontsize=16)
plt.xlabel("Number of Wins", fontsize=12)
plt.ylabel("Team", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Add data labels
for index, value in enumerate(win_counts.values):
    plt.text(value + 0.2, index, str(value), va="center", fontsize=10)

plt.tight_layout()
plt.savefig("ipl_2020_wins_per_team.png")
plt.show()

# Step 4: Visualization 2 - Stacked Bar Chart: Match Outcomes by Place
# Create a new column to categorize outcomes
df["outcome"] = df["winner"].apply(lambda x: "Tie" if x == "Tie" else "Win")

# Group by place and outcome
outcome_by_place = df.groupby(["place", "outcome"]).size().unstack(fill_value=0)

# Plot stacked bar chart
plt.figure(figsize=(10, 6))
outcome_by_place.plot(kind="bar", stacked=True, color=["#1f77b4", "#ff7f0e"], figsize=(10, 6))
plt.title("IPL 2020: Match Outcomes by Place", fontsize=16)
plt.xlabel("Venue", fontsize=12)
plt.ylabel("Number of Matches", fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Outcome")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("ipl_2020_outcomes_by_place.png")
plt.show()

# Step 5: Visualization 3 - Line Chart: Wins Over Time for Top Teams
# Calculate cumulative wins for each team
teams = ["Mumbai Indians", "Delhi Capitals", "Sunrisers Hyderabad", "Kolkata Knight Riders", "Royal Challengers Bangalore", "Rajasthan Royals", "Chennai Super Kings", "Punjab Kings"]
cumulative_wins = pd.DataFrame(index=df["date"].unique())

for team in teams:
    # Filter matches where the team won
    team_wins = df[(df["winner"] == team) & (df["winner"] != "Tie")]
    # Calculate cumulative wins
    wins_over_time = team_wins.groupby("date").size().cumsum().reindex(cumulative_wins.index, fill_value=0)
    # Forward fill to show cumulative wins
    wins_over_time = wins_over_time.ffill().fillna(0)
    cumulative_wins[team] = wins_over_time

# Plot line chart
plt.figure(figsize=(14, 8))
for team in teams:
    plt.plot(cumulative_wins.index, cumulative_wins[team], marker="o", label=team)

plt.title("IPL 2020: Cumulative Wins Over Time for Each Team", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Cumulative Wins", fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("ipl_2020_wins_over_time.png")
plt.show()